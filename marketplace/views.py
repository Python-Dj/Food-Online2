from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required

from vendor.models import Vendor
from menu.models import Category, FoodItem

from .models import Cart
from .context_processors import get_cart_counter, get_cart_amount



def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    context = {
        "vendors": vendors
    }
    return render(request, "marketplace/vendor-list.html", context)


def vendor_details(request, slug):
    vendor = Vendor.objects.get(vendor_slug=slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            "fooditems",
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = []
    context = {
        "vendor": vendor,
        "categories": categories,
        "cart_items": cart_items,
    }
    return render(request, "marketplace/vendor-details.html", context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                cart, created = Cart.objects.get_or_create(user=request.user, fooditem=fooditem)
                cart.quantity += 1
                cart.save()
                if created:
                    return JsonResponse({
                        "status": "Success",
                        "message": "New food item added to your Cart!",
                        "cart_counter": get_cart_counter(request),
                        "qty": cart.quantity,
                        "cart_amount": get_cart_amount(request)
                    })
                else:
                    return JsonResponse({
                        "status": "Success",
                        "message": "Food quantity Increased!",
                        "cart_counter": get_cart_counter(request),
                        "qty": cart.quantity,
                        "cart_amount": get_cart_amount(request)
                    })
            except:
                return JsonResponse({"status": "Falied", "message": "Something is wrong with your Cart or Fooditem!"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    return JsonResponse({"status": "Login-Required", "message": "please login to continue!"})


def removeFromCart(request, pk):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(pk=pk)
                cart = Cart.objects.get(fooditem=fooditem, user=request.user)
                if cart.quantity > 0:
                    cart.quantity -= 1
                    cart.save()
                else:
                    cart.delete()
                return JsonResponse({
                        "status": "Success",
                        "cart_counter": get_cart_counter(request),
                        "qty": cart.quantity,
                        "cart_amount": get_cart_amount(request),
                    })
            except:
                return JsonResponse({"status": "Failed", "message": "This food does not exist!"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    else:
        return JsonResponse({"status": "Login-Required", "message": "please login to continue!"})


@login_required(login_url="login")
def cart(request):
    cartItems = Cart.objects.filter(user=request.user).order_by("created_at")
    return render(request, "marketplace/cart.html", {"cartItems": cartItems})


@login_required(login_url="login")
def deleteCart(request, cart_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            cart_item.delete()
            return JsonResponse({
                "status": "Success",
                "message": "Cart has been deleted Successfully!",
                "cart_counter": get_cart_counter(request),
                "cart_amount": get_cart_amount(request),
            })
        except:
            return JsonResponse({"status": "Failed", "message": "No food item to delete!"})
