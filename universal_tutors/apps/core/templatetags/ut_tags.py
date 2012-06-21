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
    
    def __init__(self, type):
        if type == 'student':
            self.type = Video.VIDEO_TYPES.STUDENTGUIDE
        elif type == 'tutor':
            self.type = Video.VIDEO_TYPES.TUTORGUIDE
    
    def render(self, context):
        try:
            context['video'] = Video.objects.filter(active=True, type=self.type).latest('id')
        except Video.DoesNotExist:
            context['video'] = None
        return ''
             
@register.tag
def get_video(parser, token):
    bits = token.split_contents()
    return TutorVideoNode(bits[1])


class ScribblarSpeedValues(template.Node):
    def render(self, context):
        context['scribblar_speed'] = settings.SCRIBBLAR_SPEED
        context['speed_test_link'] = settings.SPEED_TEST_LINK
        return ''


@register.tag
def get_scribblar_speed_test(parser, token):
    return ScribblarSpeedValues()
