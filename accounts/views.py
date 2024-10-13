from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import UserForm
from .models import User

from vendor.forms import VendorForm
from vendor.models import Vendor



def registerUser(request):
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.RoleChoice.CUSTOMER
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            messages.success(request, "Your account have been registered Successfully!")
            return redirect("register-user")

            # we can follow a different approach to create user
            # form.cleaned_data.pop("confirm_password")
            # data = form.cleaned_data
            # print(data)
            # user = User.objects.create_user(**data)
            # user.role = User.RoleChoice.CUSTOMER
            # user.save()
        else:
            return render(request, "accounts/registerUser.html", context={"form": form})

    form = UserForm()
    context = {
        "form": form
    }
    return render(request, "accounts/registerUser.html", context)


def registerVendor(request):
    if request.method == "POST":
        uform = UserForm(request.POST)
        vform = VendorForm(request.POST, request.FILES)
        if uform.is_valid() and vform.is_valid():
            uform.cleaned_data.pop("confirm_password")
            user_data = uform.cleaned_data
            user = User.objects.create_user(**user_data)
            user.role = User.RoleChoice.VENDOR
            user.save()
            vendor = vform.save(commit=False)
            vendor.user = user
            vendor.user_profile = user.user_profile
            vendor.save()
            messages.success(request, "Your account has been register succesfully! wait for the approval.")
            return redirect("register-vendor")
        else:
            context={
                "userForm": uform,
                "vendorForm": vform
            }
            return render(request, "accounts/registerVendor.html", context)
    userForm = UserForm()
    vendorForm = VendorForm()
    context = {
        "userform": userForm,
        "vendorform": vendorForm
    }
    return render(request, "accounts/registerVendor.html", context)
