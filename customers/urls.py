from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path("", AccountViews.custDashboard, name="custDashboard"),
    path("profile/", views.profile, name="customer-profile"),
    path("myOrders/", views.my_orders, name="my-orders"),
    path("orderDetails/<int:order_number>", views.order_details, name="order-details"),
]
