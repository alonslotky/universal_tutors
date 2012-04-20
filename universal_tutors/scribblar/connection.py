from django.conf import settings 
from settings import SCRIBBLAR_API_URL
import urllib, urllib2
from BeautifulSoup import BeautifulSoup

class ScribblarError(Exception): pass

def get_soup_result(*args, **kwargs):
    url = '%s?api_key=%s&%s' % (SCRIBBLAR_API_URL, settings.SCRIBBLAR_API_KEY, urllib.urlencode(kwargs))
    file = urllib2.urlopen(url)
    data = file.read()
    file.close()

    soup = BeautifulSoup(data)
    e = soup.find('error')
    if e:
        raise Exception(e['message'])

    return soup

def get_result(*args, **kwargs):
    result = []
    for item in get_soup_result(*args, **kwargs).findAll('result'):
        item_dict = {}
        for a in item.contents:
            if hasattr(a,'name'):
                item_dict[a.name] = a.string
        result.append(item_dict)  
    
    return result

