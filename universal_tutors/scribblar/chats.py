from connection import get_result, get_soup_result

def list(*args, **kwargs):
    kwargs.update({'function': 'chats.list'})
    return get_result(*args, **kwargs)

def details(*args, **kwargs):
    kwargs.update({'function': 'chats.details'})
    return get_result(*args, **kwargs)[0]
