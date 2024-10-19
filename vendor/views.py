from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Vendor
from .forms import VendorForm

from accounts.models import User, UserProfile
from accounts.forms import UserForm, UserProfileForm

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
