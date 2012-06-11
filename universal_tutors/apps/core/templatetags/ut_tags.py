from django import template
from django.conf import settings

from apps.core.models import Quote, Video

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
def get_quote(parser, token):
    return ContentQuoteNode()

@register.filter
def is_today(date):
    today = datetime.date.today()
    if hasattr(date, 'date'):
        return date.date() == today
    else:
        return date == today
    

class TutorVideoNode(template.Node):
    def render(self, context):
        try:
            context['video'] = Video.objects.filter(active=True, type=Video.VIDEO_TYPES.TUTORGUIDE).latest('id')
        except Video.DoesNotExist:
            context['video'] = None
        return ''
             
@register.tag
def get_tutor_video(parser, token):
    return TutorVideoNode()