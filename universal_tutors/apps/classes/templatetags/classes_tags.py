from django import template
from django.contrib.auth.models import User
register = template.Library()

from apps.profile.models import TutorReview
from apps.classes.settings import *
from apps.core.models import Currency

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

@register.simple_tag
def from_currency_to_currency(curr1, curr2, value):
    try:
        value = value * Currency.objects.get(acronym=curr2).value / Currency.objects.get(acronym=curr1).value
        return '%.2f' % value
    except Currency.DoesNotExist:
        return 0