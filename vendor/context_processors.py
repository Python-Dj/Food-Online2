from django.conf import settings
from .models import Vendor



def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_google_api_key(request):
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    return dict(GOOGLE_API_KEY=GOOGLE_API_KEY)