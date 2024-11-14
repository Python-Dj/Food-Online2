from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.http.response import JsonResponse
from django.db import IntegrityError

from .models import Vendor, OpeningHour
from .forms import VendorForm, OpeningHourForm
from .context_processors import get_vendor

from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodForm

from .utils import check_role_vendor




@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, "vendor/vendorDashboard.html")


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    userProfile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        userProForm = UserProfileForm(request.POST, request.FILES, instance=userProfile)
        vendorForm = VendorForm(request.POST, request.FILES, instance=vendor)
        if userProForm.is_valid() and vendorForm.is_valid():
            userProForm.save()
            vendorForm.save()
            print("save")
            messages.success(request, "Profile Updated!")
            return redirect("vendor-profile")
        else:
            return render(request, "vendor/vendor-profile.html", {
                "userProForm": userProForm,
                "vendorForm": vendorForm,
                "userProfile": userProfile,
                "vendor": vendor
            })
        
    userProForm = UserProfileForm(instance=userProfile)
    vendorForm = VendorForm(instance=vendor)
    context = {
        "userProForm": userProForm,
        "vendorForm": vendorForm,
        "userProfile": userProfile,
        "vendor": vendor
    }
    vendor = Vendor.objects.get(user=request.user)
    return render(request, "vendor/vendor-profile.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by("created_at")
    context = {"categories": categories}
    return render(request, "vendor/menu-builder.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = Category.objects.get(vendor=vendor, pk=pk)
    fooditems = FoodItem.objects.filter(category=category, vendor=vendor)
    context = {
        "fooditems": fooditems,
        "category": category,
    }
    return render(request, "vendor/fooditems-by-category.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category_name = form.cleaned_data["category_name"]
            vendor = Vendor.objects.get(user=request.user)
            category.vendor = vendor
            category.save()
            category.slug = slugify(category_name) + "-" + str(category.id)
            category.save()
            messages.success(request, "A new category has been added!")
            return redirect("menu-builder")
        else:
            return render(request, "vendor/add-category.html", {"form": form})
    form = CategoryForm()
    return render(request, "vendor/add-category.html", {"form": form})


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = Category.objects.get(pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category_name = form.cleaned_data["category_name"]
            vendor = Vendor.objects.get(user=request.user)
            category.vendor = vendor
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "A new category has been added!")
            return redirect("menu-builder")
        else:
            return render(request, "vendor/add-category.html", {"form": form})
        
    form = CategoryForm(instance=category)
    context = {
        "category": category,
        "form": form
    }
    return render(request, "vendor/edit-category.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = Category.objects.get(pk=pk)
    category.delete()
    messages.success(request, "Category deleted Successfully!")
    return redirect("menu-builder")


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = Vendor.objects.get(user=request.user)
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.vendor = vendor
            food.slug = slugify(food_title)
            food.save()
            messages.success(request, "Food Item added Successfully!")
            return redirect("fooditems-by-category", food.category.id)
        else:
            return render(request, "vendor/add-food.html", {"form": form})
    form = FoodForm()
    vendor = Vendor.objects.get(user=request.user)
    form.fields["category"].queryset = Category.objects.filter(vendor=vendor)
    context = {
        "form": form
    }
    return render(request, "vendor/add-food.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            food = form.save(commit=False)
            vendor = get_object_or_404(Vendor, user=request.user)
            food_title = form.cleaned_data["food_title"]
            food.vendor = vendor
            food.slug = slugify(food_title)
            food.save()
            messages.success(request, "Fooditem updated Successfully!")
            return redirect("fooditems-by-category", food.category.id)
        else:
            return render(request, "vendor/edit-food.html", {"food": food, "form": form})
    form = FoodForm(instance=food)
    vendor = Vendor.objects.get(user=request.user)
    form.fields["category"].queryset = Category.objects.filter(vendor=vendor)
    context = {
        "form": form,
        "food": food
    }
    return render(request, "vendor/edit-food.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def delete_fooditem(request, pk=None):
    vendor = get_object_or_404(Vendor, user=request.user)
    food = get_object_or_404(FoodItem, pk=pk, vendor=vendor)
    food.delete()
    messages.success(request, "FoodItem deleted Successfully!")
    return redirect("fooditems-by-category", food.category.id)



def opening_hours(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    op_hrs = OpeningHour.objects.filter(vendor=vendor)
    form = OpeningHourForm()
    context = {
        "op_hrs": op_hrs,
        "form": form,
    }
    return render(request, "vendor/opening-hours.html", context)


def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "POST":
            day = request.POST.get("day")
            from_hour = request.POST.get("from_hour")
            to_hour = request.POST.get("to_hour")
            is_closed = request.POST.get("is_closed")
            try:
                vendor = get_object_or_404(Vendor, user=request.user)
                opening_hours = OpeningHour.objects.create(
                    vendor=vendor,
                    day=day,
                    from_hour=from_hour,
                    to_hour=to_hour,
                    is_closed=is_closed
                )
                if opening_hours:
                    op_hrs = OpeningHour.objects.get(id=opening_hours.id)
                    if op_hrs.is_closed:
                        response = {"status": "success", "id": op_hrs.id, "day": op_hrs.get_day_display(), "is_closed": "closed"}
                    else:
                        response = {"status": "success", "id": op_hrs.id, "day": op_hrs.get_day_display(), "from_hour": op_hrs.from_hour, "to_hour": op_hrs.to_hour}
                    return JsonResponse(response)
            except IntegrityError as e:
                response = {"status": "failed", "message": "this opening hours for this day is alredy exists!"}
                return JsonResponse(response)
        else:
            return JsonResponse("Invalid Request!")


def remove_opening_hours(request, pk):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                opening_hour = OpeningHour.objects.get(id=pk)
                opening_hour.delete()
                response = {"status": "success", "message": "Opening hour has been removed!", "id": pk}
                return JsonResponse(response)
            except:
                return JsonResponse({"staus": "failed", "message": "not a valid opening hours ID!"})
        response = {"status": "failed", "message": "Invalid!"}
        return JsonResponse(response)