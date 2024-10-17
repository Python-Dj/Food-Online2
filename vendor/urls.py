from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.vendorDashboard, name="vendor-dashboard"),
    path("profile/", views.vendorProfile, name="vendor-profile"),
]
