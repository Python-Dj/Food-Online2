from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import simplejson as json
from decimal import Decimal

from .forms import UserInfoForm

from accounts.forms import UserProfileForm
from accounts.models import User, UserProfile
from orders.models import Order, OrderedFood


@login_required(login_url="login")
def profile(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)

    user_form = UserInfoForm(instance=user)
    profile_form = UserProfileForm(instance=userProfile)

    if request.method == "POST":
        user_form = UserInfoForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userProfile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("customer-profile")
        else:
            context = {
                "user_form": user_form,
                "profile_form": profile_form,
                "user": user
            }
            return render(request, "customers/profile.html", context)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user": user
    }
    return render(request, "customers/profile.html", context)


@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by("-created_at")
    context = {
        "orders": orders
    }
    return render(request, "customers/my-orders.html", context)


@login_required(login_url="login")
def order_details(request, order_number):
    try:
        order = Order.objects.get(is_ordered=True, order_number=order_number)
        tax_data = json.loads(order.tax_data)
        ordered_foods = OrderedFood.objects.filter(order=order)
        sub_total = order.total - order.total_tax 
        context = {
            "order": order,
            "tax_data": tax_data,
            "sub_total": sub_total,
            "ordered_foods": ordered_foods
        }
        return render(request, "customers/order-details.html", context)
    except:
        return redirect("my-orders")