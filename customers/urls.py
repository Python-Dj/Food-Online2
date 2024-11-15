from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path("", AccountViews.custDashboard, name="custDashboard"),
    path("profile/", views.profile, name="customer-profile"),
]
