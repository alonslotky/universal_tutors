import datetime, urllib
import simplejson as json
from apps.core.models import Currency

from ordereddict import OrderedDict

def update_currencies():
    url = 'http://openexchangerates.org/latest.json'
    
    currencies = json.load(urllib.urlopen(url))
    base = currencies['base']
    rates = currencies['rates']
    
    base_value = 1 / rates['GBP'] if base != 'GBP' else 1
    
    for currency in Currency.objects.filter(manual=False):
        currency.value = base_value * rates[currency.acronym]
        currency.save()


def get_status_from_dict(dtc, key, class_):
    try:
        status = dtc[key][class_.status]
    except:
        dtc[key] = [set() for i in xrange(10)]
        status = dtc[key][class_.status]
    return status

def add_student_to_dict(dtc, key, class_):
    get_status_from_dict(dtc, key, class_).add(class_.student.username)

def add_tutor_to_dict(dtc, key, class_):
    get_status_from_dict(dtc, key, class_).add(class_.tutor.username)

def add_class_to_dict(dtc, key, class_):
    get_status_from_dict(dtc, key, class_).add(class_.id)


def init_price_per_hour():
    d = OrderedDict()
    d['< 10 credits'] = [set() for i in xrange(10)]
    d['10 to 15 credits'] = [set() for i in xrange(10)]
    d['15 to 20 credits'] = [set() for i in xrange(10)]
    d['20 to 25 credits'] = [set() for i in xrange(10)]
    d['25 to 30 credits'] = [set() for i in xrange(10)]
    d['> 30 credits'] = [set() for i in xrange(10)]
    return d

def get_price_per_hour_slot(class_):
    if class_.credit_fee < 10: return '< 10 credits'
    if class_.credit_fee < 15: return '10 to 15 credits'
    if class_.credit_fee < 20: return '15 to 20 credits'
    if class_.credit_fee < 25: return '20 to 25 credits'
    if class_.credit_fee < 30: return '25 to 30 credits'
    if class_.credit_fee >= 30: return '> 30 credits'

def init_total_price():
    d = OrderedDict()
    d['< 10 credits'] = [set() for i in xrange(10)]
    d['10 to 15 credits'] = [set() for i in xrange(10)]
    d['15 to 20 credits'] = [set() for i in xrange(10)]
    d['20 to 25 credits'] = [set() for i in xrange(10)]
    d['25 to 30 credits'] = [set() for i in xrange(10)]
    d['30 to 35 credits'] = [set() for i in xrange(10)]
    d['35 to 40 credits'] = [set() for i in xrange(10)]
    d['40 to 45 credits'] = [set() for i in xrange(10)]
    d['45 to 50 credits'] = [set() for i in xrange(10)]
    d['> 50 credits'] = [set() for i in xrange(10)]
    return d

def get_total_price_slot(class_):
    if class_.subject.credits < 10: return '< 10 credits'
    if class_.subject.credits < 15: return '10 to 15 credits'
    if class_.subject.credits < 20: return '15 to 20 credits'
    if class_.subject.credits < 25: return '20 to 25 credits'
    if class_.subject.credits < 30: return '25 to 30 credits'
    if class_.subject.credits < 35: return '30 to 35 credits'
    if class_.subject.credits < 40: return '35 to 40 credits'
    if class_.subject.credits < 45: return '40 to 45 credits'
    if class_.subject.credits < 50: return '45 to 50 credits'
    if class_.subject.credits >= 50: return '> 50 credits'

def init_class_time():
    d = OrderedDict()
    d['30 minutes'] = [set() for i in xrange(10)]
    d['60 minutes'] = [set() for i in xrange(10)]
    d['90 minutes'] = [set() for i in xrange(10)]
    d['120 minutes'] = [set() for i in xrange(10)]
    return d

def init_currencies(): 
    d = OrderedDict()
    for currency in Currency.objects.all():
        d[currency.symbol] = {'name': currency, 'topup': 0, 'withdraw': 0}
    return d

def init_credits_evolution(items, classes):
    today = datetime.date.today()

    try:
        first_item_date = items[0].created.date()
    except IndexError:
        first_item_date = today

    try:
        first_class_date = classes[0].created.date()
    except IndexError:
        first_class_date = today

    time = min(first_item_date, first_class_date)
    
    d = OrderedDict()
    while time <= today:
        d[time.strftime('%b %Y')] = {'topup': 0, 'withdraw': 0, 'profit': 0}

    return d
