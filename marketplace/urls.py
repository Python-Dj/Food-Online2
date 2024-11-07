from django.urls import path
from . import views


urlpatterns = [
    path("", views.marketplace, name="marketplace"),
    path("<slug:slug>/", views.vendor_details, name="vendor-details"),

    # Add Cart
    path("addToCart/<int:food_id>/", views.add_to_cart, name="add-to-cart"),

    # Remove from Cart
    path("removeFromCart/<int:pk>", views.removeFromCart, name="remove-from-cart"),

    #Delete Cart
    path("deleteCart/<int:cart_id>/", views.deleteCart, name="delete-cart"),    
]
