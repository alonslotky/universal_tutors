from django.conf import settings

try:
    SCRIBBLAR_API_URL = settings.SCRIBBLAR_API_URL 
except AttributeError:
    SCRIBBLAR_API_URL = 'https://api.scribblar.com/v1/'
    
try:
    SCRIBBLAR_ASSETS_URL = settings.SCRIBBLAR_ASSETS_URL
except AttributeError:
    SCRIBBLAR_ASSETS_URL = 'http://api.muchosmedia.com/brainwave/uploads/client_%(client)s/f_%(assetid)s%(ext)s'
    
try:
    SCRIBBLAR_RECORDINGS_URL = settings.SCRIBBLAR_RECORDINGS_URL
except AttributeError:
    SCRIBBLAR_RECORDINGS_URL = 'http://replay.scribblar.com/?recid=%(recid)s'