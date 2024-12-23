from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from marketplace import views as MarketpPlaceView



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("", include("accounts.urls")),
    path("marketplace/", include("marketplace.urls")),
    
    # CART 
    path("cart/", MarketpPlaceView.cart, name="cart"),

    # Search
    path('search/', MarketpPlaceView.search, name="search"),
    path("customer/", include("customers.urls")),

    #CHECKOUT
    path("checkout/", MarketpPlaceView.checkout, name="checkout"),

    #Order
    path("orders/", include("orders.urls")),
    
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
