from django.shortcuts import redirect, render

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance 

from vendor.models import Vendor


def get_or_create_current_location(request):
    if request.session:
        longitude = request.session.get('lng')
        latitude = request.session.get('lat')
        # print(dict(request.session))

        pnt = GEOSGeometry("POINT({lng} {lat})".format(lng=longitude, lat=latitude), srid=4326)
        return pnt
    elif request.GET:
        longitude = request.GET.get('longitude')
        latitude = request.GET.get('latitude')

        # saving lat and lng in session
        request.session['lat'] = latitude
        request.session['lng'] = longitude

        pnt = GEOSGeometry("POINT({lng} {lat})".format(lng=longitude, lat=latitude), srid=4326)
        return pnt
    else:
        return None



def home(request):
    pnt = get_or_create_current_location(request)
    if pnt:
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=100))).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
        for v in vendors:
            v.kms = round(v.distance.km, 1)
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    return render(request, "home.html", {"vendors": vendors})