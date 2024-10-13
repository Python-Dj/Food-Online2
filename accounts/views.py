from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import UserForm
from .models import User




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
