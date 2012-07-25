from django import template
from django.contrib.auth.models import User
register = template.Library()

from apps.profile.models import TutorReview
from apps.classes.settings import *

@register.filter
def in_currency(value, currency):
    try:
        return value * currency.credit_value()
    except AttributeError:
        return 0

@register.filter
def discount(value, d):
    return value * (1 - d)

@register.filter
def rec_url(class_, id):
    try:
        return class_.get_rec_url(id)
    except AttributeError:
        return ''
