from connection import get_result, get_soup_result
from settings import SCRIBBLAR_RECORDINGS_URL

def list(*args, **kwargs):
    kwargs.update({'function': 'recordings.list'})
    return get_result(*args, **kwargs)

def listbyroom(*args, **kwargs):
    kwargs.update({'function': 'recordings.listbyroom'})
    return get_result(*args, **kwargs)

def delete(*args, **kwargs):
    kwargs.update({'function': 'recordings.delete'})
    return get_result(*args, **kwargs)[0]

def details(*args, **kwargs):
    kwargs.update({'function': 'recordings.details'})
    return get_result(*args, **kwargs)[0]

def url(*args, **kwargs):
    recid = kwargs.pop('recid')
    return SCRIBBLAR_RECORDINGS_URL % {'recid': recid}