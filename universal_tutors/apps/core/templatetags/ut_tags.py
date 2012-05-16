from django import template
from django.conf import settings

from apps.core.models import Quote

import datetime, random

register = template.Library()

class ContentQuoteNode(template.Node):
    def render(self, context):
        context['quote'] = random.choice(Quote.objects.all())
        return ''

@register.tag
def get_quote(pareser, token):
    return ContentQuoteNode()    