import datetime, urllib, urllib2
import simplejson as json
from django.conf import settings
from apps.core.models import *
from apps.common.utils.fields import COUNTRIES

from ordereddict import OrderedDict
from scribblar import users
import pytz


def update_currencies():
    url = 'http://openexchangerates.org/api/latest.json?app_id=%s' % settings.OPENXCHANGE_API_KEY
    
    currencies = json.load(urllib2.urlopen(url))
    base = currencies['base']
    rates = currencies['rates']
    
    base_value = 1 / rates['GBP'] if base != 'GBP' else 1
    
    for currency in Currency.objects.filter(manual=False):
        value = base_value * rates[currency.acronym]
        currency.value = value + value * (settings.CURRENCY_RISK if currency.acronym != 'GBP' else 0)
        currency.save()


def get_invisible_user():
    scribblar_default_username = 'ut_inv_user_role_150'
    scribblar_user = None
    for s_user in users.list():
        if s_user.get('username', '').lower() == scribblar_default_username:
            scribblar_user = s_user
            break

    if not scribblar_user:
        scribblar_user = users.add(
            username = scribblar_default_username,
            firstname = 'Universal',
            lastname = 'Tutors',
            roleid = 150,
        )
    
    return scribblar_user

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
    if class_.subject_credits_per_hour < 10: return '< 10 credits'
    if class_.subject_credits_per_hour < 15: return '10 to 15 credits'
    if class_.subject_credits_per_hour < 20: return '15 to 20 credits'
    if class_.subject_credits_per_hour < 25: return '20 to 25 credits'
    if class_.subject_credits_per_hour < 30: return '25 to 30 credits'
    if class_.subject_credits_per_hour < 35: return '30 to 35 credits'
    if class_.subject_credits_per_hour < 40: return '35 to 40 credits'
    if class_.subject_credits_per_hour < 45: return '40 to 45 credits'
    if class_.subject_credits_per_hour < 50: return '45 to 50 credits'
    if class_.subject_credits_per_hour >= 50: return '> 50 credits'

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
        time = time.replace(year=time+1, month=1) if time.month == 12 else time.replace(month=time.month+1)

    return d




### TIMEZONE #########
def init_timezones():
    for id, name in COUNTRIES:
        Country.objects.get_or_create(country=id, country_name=name)
    for timezone in pytz.all_timezones:
        Timezone.objects.get_or_create(timezone=timezone)

