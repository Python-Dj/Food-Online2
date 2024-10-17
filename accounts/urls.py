from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    # path("admin/", admin.site.urls),
    path("registerUser/", views.registerUser, name="register-user"),
    path("registerVendor/",views.registerVendor, name="register-vendor"),

    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("myAccount/", views.myAccount, name="myAccount"),
    path("custDashboard/", views.custDashboard, name="custDashboard"),
    # path("vendorDashboard/", views.vendorDashboard, name="vendorDashboard"),
    
    #* Account activation path
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    #* Forgot Password releted path
    path("forgotPassword/", views.forgotPassword, name="forgot-password"),
    path("resetPasswordValidate/<uidb64>/<token>", views.resetPasswordValidate, name="reset-password-validate"),
    path("resetPassword/", views.resetPassword, name="reset-password"),

    #* urls releated to vendor app.
    path("vendor/", include("vendor.urls")),
]
