from django.urls import path
from . import views


urlpatterns = [
    path("placeOrder/", views.place_order, name="place-order"),
    path("payments/", views.payments, name="payments"),
    path("orderComplete/", views.order_complete, name="order-complete"),
]
