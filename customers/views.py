from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserInfoForm
from accounts.forms import UserProfileForm

from accounts.models import User, UserProfile


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
