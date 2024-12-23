from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Prefetch, Q
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from vendor.models import Vendor
from accounts.models import UserProfile
from menu.models import Category, FoodItem
from vendor.models import OpeningHour
from orders.forms import OrderForm
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
    # Opening Hours
    op_hrs = OpeningHour.objects.filter(vendor=vendor)
    today_day = datetime.today().isoweekday()
    today_op_hrs = op_hrs.filter(day=today_day)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = []
    context = {
        "vendor": vendor,
        "categories": categories,
        "cart_items": cart_items,
        "op_hrs": op_hrs,
        "today_op_hrs": today_op_hrs
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
                response = {
                    "status": "Success",
                    "message": "Food quantity Increased!",
                    "cart_counter": get_cart_counter(request),
                    "qty": cart.quantity,
                    "cart_amount": get_cart_amount(request)
                }
                return JsonResponse(response)
            except Exception as e:
                return JsonResponse({"status": "Falied", "message": "Fooditem dosen't exist!"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    return JsonResponse({"status": "Login-Required", "message": "please login to continue!"})


def removeFromCart(request, pk):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(pk=pk)
                cart = Cart.objects.get(fooditem=fooditem, user=request.user)
                if cart.quantity:
                    cart.quantity -= 1
                    cart.save()
                if cart.quantity == 0:
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
        

def search(request):
    if not 'address' in request.GET:
        return redirect("marketplace")
    else:
        keyword = request.GET["keyword"]
        address = request.GET["address"]
        latitude = request.GET["lat"]
        longitude = request.GET["lng"]
        radius = request.GET["radius"]

        # get vendor id that has the fooditem user is looking for
        get_vendor_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)

        if longitude and longitude and radius:
            pnt = GEOSGeometry("POINT({lng} {lat})".format(lng=longitude, lat=latitude), srid=4326)
            vendors = Vendor.objects.filter(
                Q(is_approved=True, vendor_name__icontains=keyword, user__is_active=True) | Q(id__in=get_vendor_by_fooditems),
                user_profile__location__distance_lte=(pnt, D(km=radius)),
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)
        vendors_count = vendors.count()
        context = {
            "vendors": vendors,
            "vendors_count": vendors_count,
            "source_location": address
        }
        return render(request, "marketplace/vendor-list.html", context)


@login_required(login_url="login")
def checkout(request):
    cartItems = Cart.objects.filter(user=request.user).order_by("created_at")
    cart_count = cartItems.count()
    if cart_count <= 0:
        return redirect("marketplace")
    
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    default_values = {
        "first_name": user.firstName,
        "last_name": user.lastName,
        "email": user.email,
        "phone": user.phone_number,
        "address": user_profile.address,
        "country": user_profile.country,
        "state": user_profile.state,
        "city": user_profile.city,
        "pin_code": user_profile.pin_code
    }
    form = OrderForm(initial=default_values)
    context = {
        "form": form,
        "cartItems": cartItems,
    }
    return render(request, "marketplace/checkout.html", context)