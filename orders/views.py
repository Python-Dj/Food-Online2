import razorpay

from django.shortcuts import render, redirect
import simplejson as json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from marketplace.context_processors import get_cart_amount
from marketplace.models import Cart, Tax
from menu.models import FoodItem

from vendor.utils import send_notification

from .models import Order, Payment, OrderedFood
from .forms import OrderForm
from .utils import generate_order_number


client = razorpay.Client(auth=(settings.RZP_KEY_ID, settings.RZP_KEY_SECRET))


@login_required(login_url="login")
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("marketplace")
    
    vendors_id = []
    for item in cart_items:
        if item.fooditem.vendor.id not in vendors_id:
            vendors_id.append(item.fooditem.vendor.id)

    # data = {"vendor_id": {"subtotal": "amount", "tax_type": {"tax_percentage": "tax_amount"}}}
    get_tax = Tax.objects.filter(is_active=True)
    total_data = {}
    for item in cart_items:
        fooditem = FoodItem.objects.get(id=item.fooditem.id, vendor__id__in=vendors_id)
        if fooditem.vendor.id in total_data:
            total_data[fooditem.vendor.id]["subtotal"] += (fooditem.price * item.quantity)
        else:
            total_data[fooditem.vendor.id] = {"subtotal": (fooditem.price * item.quantity)}
        
        # Calculte tax data
        for tax in get_tax:
            subtotal = total_data[fooditem.vendor.id]["subtotal"]
            tax_amount = round((subtotal * tax.tax_percentage/100), 2)
            total_data[fooditem.vendor.id][tax.tax_type] = {str(tax.tax_percentage): str(tax_amount)}
    
    # Updating subtotal value Decimal to String.
    for vendor_id in total_data:
        total_data[vendor_id]["subtotal"] = str(total_data[vendor_id]["subtotal"])

    
    cart_amounts = get_cart_amount(request)
    # sub_total = cart_amounts["subTotal"]
    tax_amount = cart_amounts["tax"]
    grand_total = cart_amounts["grandTotal"]
    tax_data = cart_amounts["all_taxes"]
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            pay_method = request.POST.get("payment_method")
            order = form.save(commit=False)
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.total_tax = tax_amount
            order.payment_method = pay_method
            order.save()

            # Now order Id has been generate, we can add order_number
            order.order_number = generate_order_number(order.id)

            order.vendors.add(*vendors_id)
            order.save()

            #Razorpay payment Data
            DATA = {
                "amount": round(float(order.total)*100),
                "currency": "INR",
                "receipt": "order_receipt #"+order.order_number
            }
  
            rzp_order = client.order.create(data=DATA)
            rzp_order_id = rzp_order["id"]
            
            context = {
                "order": order,
                "cart_items": cart_items,
                "rzp_order_id": rzp_order_id,
                "RZP_KEY_ID": settings.RZP_KEY_ID,
                "rzp_amount": round(float(order.total)*100),
            }
            return render(request, "orders/place-order.html", context)
        else:
            print(form.errors)
    return render(request, "orders/place-order.html")


@login_required(login_url="login")
def payments(request):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "POST":
            data = request.POST
            transaction_id = data.get("transaction_id")
            payment_method = data.get("payment_method")
            status = data.get("status")
            order_number =  data.get("order_number")

            order = Order.objects.get(user=request.user, order_number=order_number)
            payment = Payment.objects.create(
                user = request.user,
                transaction_id = transaction_id,
                payment_method = payment_method,
                status = status,
                amount = order.total
            )

            # Update the order Model
            order.payment = payment
            order.is_ordered = True
            order.save()

            # Move the Cart item into OrderedFood Model
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                ordered_food = OrderedFood(
                    order=order,
                    payment=payment,
                    user=request.user,
                    fooditem=item.fooditem,
                    quantity=item.quantity,
                    price=item.fooditem.price,
                    amount=item.quantity*item.fooditem.price,
                )
                ordered_food.save()

            # SEND ORDER CONFIRMATION EMAIL TO CUSTOMER.
            mail_subject = "Thank you for ordering food with us."
            mail_template = "orders/order-confirmation-email.html"
            ordered_food = OrderedFood.objects.filter(order=order)
            customer_subtotal = 0
            for food in ordered_food:
                customer_subtotal += (food.price * food.quantity)
            tax_data = json.loads(order.tax_data)
            context = {
                "user": request.user,
                "order": order,
                "ordered_food": ordered_food,
                "to_email": order.email,
                "domain": get_current_site(request),
                "subtotal": customer_subtotal,
                "tax_data": tax_data,
            }
            send_notification(mail_subject, mail_template, context)

            # SEND ORDER RECEIVED EMAIL TO VENDOR.
            mail_subject = "You have received a new Order."
            mail_template = "orders/order-receive-email.html"
            to_emails = []
            for item in cart_items:
                email = item.fooditem.vendor.user.email
                if email not in to_emails:
                    to_emails.append(email)
            print(to_emails)
            context = {
                "order": order,
                "to_email": to_emails
            }
            send_notification(mail_subject, mail_template, context)

            # after successfully generated order and payment clearing the Cart.
            cart_items.delete()

            response = {
                "order_number": order_number,
                "transaction_id": transaction_id
            }
            return JsonResponse(response)
    return HttpResponse("Payment Unsuccessfull!")


def order_complete(request):
    oreder_no = request.GET.get("order_no")
    trans_id = request.GET.get("trans_id")

    try:
        order = Order.objects.get(order_number=oreder_no, payment__transaction_id=trans_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        all_taxes = json.loads(order.tax_data)
        sub_total = 0
        for item in ordered_food:
            item_total = item.price * item.quantity
            sub_total += item_total
            print(sub_total)

        context ={
            "order": order,
            "ordered_food": ordered_food,
            "sub_total": f"{sub_total:.2f}",
            "all_taxes": all_taxes
        }
        return render(request, "orders/order-complete.html", context)
    except:
        return redirect("home")


