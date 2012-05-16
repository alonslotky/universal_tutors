import datetime, urllib
import simplejson as json
from apps.core.models import Currency

def update_currencies():
    url = 'http://openexchangerates.org/latest.json'
    
    currencies = json.load(urllib.urlopen(url))
    base = currencies['base']
    rates = currencies['rates']
    
    base_value = 1 / rates['GBP'] if base != 'GBP' else 1
    
    for currency in Currency.objects.filter(manual=False):
        currency.value = base_value * rates[currency.acronym]
        currency.save()
    