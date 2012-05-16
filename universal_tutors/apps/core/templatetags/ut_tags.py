from django import template
from django.conf import settings

from apps.core.models import Quote

import datetime, random

register = template.Library()

class ContentQuoteNode(template.Node):
    def render(self, context):
        try:
            context['quote'] = random.choice(Quote.objects.all())
        except IndexError:
            context['quote'] = None
        return ''

@register.tag
def get_quote(pareser, token):
    return ContentQuoteNode()

@register.filter
def is_today(date):
    today = datetime.date.today()
    if hasattr(date, 'date'):
        return date.date() == today
    else:
        return date == today
