from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.vendorDashboard, name="vendor-dashboard"),
    path("profile/", views.vendorProfile, name="vendor-profile"),
    path("menuBuilder/", views.menu_builder, name="menu-builder"),
    path("fooditemsByCategory/<int:pk>", views.fooditems_by_category, name="fooditems-by-category"),

    #Category CRUD
    path("menuBuilder/addCategory/", views.add_category, name="add-category"),
    path("menuBuilder/editCategory/<int:pk>", views.edit_category, name="edit-category"),
    path("menuBuilder/deleteCategory/<int:pk>", views.delete_category, name="delete-category"),

    # FoodItem CRUD
    path("menuBuilder/addFood/", views.add_food, name="add-food"),
    path("menuBuilder/editFood/<int:pk>", views.edit_food, name="edit-food"),
    path("menuBuilder/deleteFood/<int:pk>", views.delete_fooditem, name="delete-fooditem"),

    # Opening Hours CRUD
    path("openingHours/", views.opening_hours, name="opening-hours"),
    path("openingHours/add/", views.add_opening_hours, name="add-opening-hours"),
    path("openingHours/remove/<int:pk>/", views.remove_opening_hours, name="remove-opening-hours"),

    path("orderDetails/<int:order_number>/", views.order_details, name="vendor-order-details"),
    path("orders/", views.orders, name="orders"),
]
