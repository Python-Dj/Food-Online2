from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Vendor

from .utils import check_role_vendor




@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, "vendor/vendorDashboard.html")


def vendorProfile(request):
    vendor = Vendor.objects.get(user=request.user)
    return render(request, "vendor/vendor-profile.html")
