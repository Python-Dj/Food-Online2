from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.template.defaultfilters import slugify

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator

from .forms import UserForm
from .models import User

from vendor.forms import VendorForm
from vendor.models import Vendor
from orders.models import Order

from .utils import detectUser, send_varification_email, check_role_customer



    


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are alredy logged in")
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

            #? Send varification email to User
            mail_subject = "Please activate your account."
            email_template = "accounts/emails/verifyAccount.html"
            send_varification_email(request, user, mail_subject, email_template)
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
        messages.warning(request, "You are alredy logged in")
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
            vendor_name = vform.cleaned_data["vendor_name"]
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            vendor.user_profile = user.user_profile
            vendor.save()

            #? Send varification email to User
            mail_subject = "Please activate your account."
            email_template = "accounts/emails/verifyAccount.html"
            send_varification_email(request, user, mail_subject, email_template)
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


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status is True.
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active =True
        user.save()
        messages.success(request, "Congratulation! your account has been Activated.")
        return redirect("myAccount")
    else:
        messages.error(request, "Invalid activation link.")
        

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are alredy logged in")
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
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by("-created_at")[:5]
    recent_orders = Order.objects.filter(user=request.user, is_ordered=True).order_by("-created_at")[:5]
    total_orders = orders.count()
    context = {
        "orders": orders,
        "recent_orders": recent_orders,
        "total_orders": total_orders,
    }
    return render(request, "accounts/custDashboard.html", context)


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            #* Send reset email link.
            email_subject = "Reset your Password"
            email_template = "accounts/emails/passwordReset.html"
            send_varification_email(request, user, email_subject, email_template)
            messages.success(request, "Password reset link hse been sent to your email!")
            return redirect("login")
        else:
            messages.error(request, "There is no account with this email.")
            return redirect("forgot-password")
    return render(request, "accounts/forgot-password.html")

def resetPasswordValidate(request, uidb64, token):
    #* Varifying the user uid and token for reset password.
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(id=uid)
    except(ValueError, TypeError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password")
        return redirect("reset-password")
    else:
        messages.error(request, "This link has been expire, try again!")
        redirect("forgot-password")

def resetPassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = request.session["uid"]
            user = User.objects.get(id=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "your password has been reset successfully!")
            return redirect("login")
        else:
            messages.error(request, "Password do not match, try again!")
            return redirect("reset-password")
    return render(request, "accounts/reset-password.html")