from .models import Cart
from menu.models import FoodItem



def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
            for cart_item in cart_items:
                cart_count += cart_item.quantity
    return dict(cart_count=cart_count)


def get_cart_amount(request):
    subTotal = 0
    tax = 0
    grandTotal = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            foodItem = FoodItem.objects.get(pk=item.fooditem.id)
            subTotal += (foodItem.price * item.quantity)
        grandTotal = subTotal + tax
    return dict(subTotal=subTotal, tax=tax, grandTotal=grandTotal)