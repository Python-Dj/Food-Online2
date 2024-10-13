from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.core.exceptions import PermissionDenied

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import UserForm
from .models import User

from vendor.forms import VendorForm
from vendor.models import Vendor

from .utils import detectUser


# Restric the vendor from accessing customer page.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
# Restrict the custome from accessing vendor page.
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning("You are alredy logged in")
        return redirect("myAccount")
    elif request.method == "POST":
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
    if request.user.is_authenticated:
        messages.warning("You are alredy logged in")
        return redirect("myAccount")
    elif request.method == "POST":
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


def login(request):
    if request.user.is_authenticated:
        messages.warning("You are alredy logged in")
        return redirect("myAccount")
    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in now!")
            return redirect("myAccount")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out!")
    return redirect("login")


@login_required(login_url="login")
def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)


@login_required(login_url="login")
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, "accounts/custDashboard.html")


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, "accounts/vendorDashboard.html")