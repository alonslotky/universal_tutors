from connection import get_result, get_soup_result
from settings import SCRIBBLAR_ASSETS_URL
import os

def list(*args, **kwargs):
    kwargs.update({'function': 'assets.list'})
    return get_result(*args, **kwargs)

def add(*args, **kwargs):
    kwargs.update({'function': 'assets.add'})
    return get_result(*args, **kwargs)[0]

def details(*args, **kwargs):
    kwargs.update({'function': 'assets.details'})
    return get_result(*args, **kwargs)[0]

def url(*args, **kwargs):
    client = kwargs.pop('client')
    assetid = kwargs.pop('assetid')
    result = details(assetid=assetid)
    try:
        return SCRIBBLAR_ASSETS_URL % {'client': client, 'assetid': assetid, 'ext': os.path.splitext(result['clientfilename'])[1] }
    except IndexError:
        return SCRIBBLAR_ASSETS_URL % {'client': client, 'assetid': assetid, 'ext': '' }
        