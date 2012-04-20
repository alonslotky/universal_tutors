from connection import get_result, get_soup_result

def list(*args, **kwargs):
    kwargs.update({'function': 'assets.list'})
    return get_result(*args, **kwargs)

def add(*args, **kwargs):
    kwargs.update({'function': 'assets.add'})
    return get_result(*args, **kwargs)[0]

def details(*args, **kwargs):
    kwargs.update({'function': 'assets.details'})
    return get_result(*args, **kwargs)[0]
