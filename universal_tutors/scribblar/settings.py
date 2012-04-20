from django.conf import settings

try:
    SCRIBBLAR_API_URL = settings.SCRIBBLAR_API_URL 
except AttributeError:
    SCRIBBLAR_API_URL = 'https://api.scribblar.com/v1/'