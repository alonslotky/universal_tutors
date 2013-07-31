from connection import get_result

def details(*args, **kwargs):
    kwargs.update({'function': 'account.details'})
    return get_result(*args, **kwargs)[0]
    
def edit(dct):
    kwargs.update({'function': 'account.edit'})
    return get_result(*args, **kwargs)[0]
