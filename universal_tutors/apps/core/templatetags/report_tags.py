from django import template
from django.conf import settings

from apps.core.models import Quote, Video
from apps.classes.models import Class

import datetime, random

register = template.Library()

@register.inclusion_tag('core/reports/_render_user_per_classes_status.html')
def render_user_per_classes_status(dtc, title, ordering=0, verbose=None):
    if ordering:
        items = sorted([(key, value) for key, value in dtc.items()], key=lambda x: x[0])
    else:
        items = [(key, value) for key, value in dtc.items()]
    
    return {
        'title': title,
        'verbose': verbose,
        'items': items,
        'STATUS': Class.STATUS_TYPES,
        'id': datetime.datetime.now().strftime("%S%f"),
    }

@register.inclusion_tag('core/reports/_render_user_classes.html')
def render_user_classes(total_users, no_users, title=None, verbose=None):
    return {
        'total': total_users,
        'users': no_users,
        'title': title,
        'verbose': verbose,
        'id': datetime.datetime.now().strftime("%S%f"),
    }

@register.inclusion_tag('core/reports/_render_user_signup.html')
def render_user_signup(total_users, no_users, title=None, verbose=None):
    return {
        'total': total_users,
        'users': no_users,
        'title': title,
        'verbose': verbose,
        'id': datetime.datetime.now().strftime("%S%f"),
    }

@register.inclusion_tag('core/reports/_render_class_status.html')
def render_class_status(data, title=None):
    return {
        'data': data,
        'title': title,
        'STATUS': Class.STATUS_TYPES,
        'id': datetime.datetime.now().strftime("%S%f"),
    }

@register.inclusion_tag('core/reports/_render_credit_movements.html')
def render_credit_movements(topup, withdraw, profit, title=None):
    return {
        'topup': topup,
        'withdraw': withdraw,
        'profit': profit,
        'title': title,
        'id': datetime.datetime.now().strftime("%S%f"),
    }

@register.inclusion_tag('core/reports/_render_value_movements.html')
def render_value_movements(currency, title=None, verbose=None):
    return {
        'currency': currency,
        'id': datetime.datetime.now().strftime("%S%f"),
    }

@register.inclusion_tag('core/reports/_render_credit_evolution.html')
def render_credit_evolution(credits_evolution, title=None):
    return {
        'credits_evolution': credits_evolution,
        'id': datetime.datetime.now().strftime("%S%f"),
    }

