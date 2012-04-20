from connection import get_result, get_soup_result

def list(*args, **kwargs):
    kwargs.update({'function': 'rooms.list'})
    return get_result(*args, **kwargs)
    
def count(*args, **kwargs):
    kwargs.update({'function': 'rooms.count'})
    soup = get_soup_result(*args, **kwargs)
    count = soup.find('count')
    return int(count.string)

def add(*args, **kwargs):
    kwargs.update({'function': 'rooms.add'})
    return get_result(*args, **kwargs)[0]

def delete(*args, **kwargs):
    kwargs.update({'function': 'rooms.delete'})
    return get_result(*args, **kwargs)[0]

def edit(*args, **kwargs):
    kwargs.update({'function': 'rooms.edit'})
    return get_result(*args, **kwargs)[0]

def details(*args, **kwargs):
    kwargs.update({'function': 'rooms.details'})
    return get_result(*args, **kwargs)[0]
