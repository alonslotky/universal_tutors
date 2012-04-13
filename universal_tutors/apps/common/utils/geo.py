from django.utils import simplejson
from django.conf import settings
from math import *

import urllib, pygeoip


def calc_bounding_box(lat, lon, radius, use_miles = True):    
    """ retval -> lat_min, lat_max, lon_min, lon_max 
        Calculates the max and min lat and lon for an area.
        It approximates a search area of radius r by using a box
        For further details:
        http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates (section 3.3)
        For testing output
        http://www.getlatlon.com/
    """
    
    # d = distance
    # R = Radius of sphere (6378.1 km or 3,963.1676 miles)
    # r = d/R angular radius of query circle

    R_MILES = 3963.1676
    R_KM    = 6378.1
    
    lat = float(radians(lat))
    lon = float(radians(lon))
    radius = float(radius)
    
    R = use_miles and R_MILES or R_KM
    
    r = radius / R
    
    lat_T = asin( sin(lat) / cos(r) )
    delta_lon = asin( sin(r) / cos(lat) )
    
    lon_min = degrees(lon - delta_lon)
    lon_max = degrees(lon + delta_lon)
    
    lat_min = degrees(lat - r)
    lat_max = degrees(lat + r)
    
    return lat_min, lat_max, lon_min, lon_max

def geocode_location(location):
    key = settings.GOOGLE_MAPS_API_KEY
    output = "json"
    location = urllib.quote_plus(location)
    request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
    data = urllib.urlopen(request).read()
    dlist = simplejson.loads(data)
    if dlist['Status']['code'] == 200:
        long = float(dlist['Placemark'][0]['Point']['coordinates'][0])
        lat = float(dlist['Placemark'][0]['Point']['coordinates'][1])
        return (lat, long)
    else:
        return (0, 0)

def get_user_location(request):
    user_location = request.COOKIES.get('user_location', None)
    if not user_location:
        gi = pygeoip.GeoIP(settings.SITE_ROOT + '/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if not ip:
            ip = request.META.get('REMOTE_ADDR')
        if settings.DEBUG and settings.DEBUG_SIMULATE_IP:
            ip = settings.DEBUG_SIMULATE_IP

        for x in ip.split(','):
            if len(x.split('.')) == 4:
                city = gi.record_by_addr(x)
                if city and city.get('latitude') and city.get('longitude') and city.get('country_code'):
                    user_location = city
                    break

    return user_location