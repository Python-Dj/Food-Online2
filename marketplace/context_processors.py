from .models import Cart, Tax
from menu.models import FoodItem



def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amount(request):
    subTotal = 0
    tax = 0
    grandTotal = 0
    all_taxes = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            foodItem = FoodItem.objects.get(pk=item.fooditem.id)
            subTotal += (foodItem.price * item.quantity)

        taxes = Tax.objects.filter(is_active=True)
        for tax in taxes:
            tax_type = tax.tax_type
            tax_percentage = tax.tax_percentage
            tax_amount = round((tax_percentage*subTotal)/100, 2)
            all_taxes.update({tax_type: {str(tax_percentage): tax_amount}})

        # total tax
        tax = 0
        for type in all_taxes.values():
            for tax_amount in type.values():
                tax = tax + tax_amount  
        grandTotal = subTotal + tax
    return dict(subTotal=subTotal, tax=tax, grandTotal=grandTotal, all_taxes=all_taxes)