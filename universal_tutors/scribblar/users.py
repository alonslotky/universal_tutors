from connection import get_result, get_soup_result

def list(*args, **kwargs):
    kwargs.update({'function': 'users.list'})
    return get_result(*args, **kwargs)
    
def count(*args, **kwargs):
    kwargs.update({'function': 'users.count'})
    soup = get_soup_result(*args, **kwargs)
    count = soup.find('count')
    return int(count.string)

def add(*args, **kwargs):
    kwargs.update({'function': 'users.add'})
    return get_result(*args, **kwargs)[0]

def delete(*args, **kwargs):
    kwargs.update({'function': 'users.delete'})
    return get_result(*args, **kwargs)[0]

def edit(*args, **kwargs):
    kwargs.update({'function': 'users.edit'})
    return get_result(*args, **kwargs)[0]

def details(*args, **kwargs):
    kwargs.update({'function': 'users.details'})
    return get_result(*args, **kwargs)[0]
