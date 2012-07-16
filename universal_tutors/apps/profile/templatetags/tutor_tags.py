from django import template
from django.contrib.auth.models import User
register = template.Library()

from apps.profile.models import TutorReview
from apps.classes.settings import *

@register.filter
def get_new_schedule_period_size(period):
    HOUR_SIZE = 4
    MARGIN_LEFT = 4
     
    # begin position
    begin = MARGIN_LEFT + period.begin.hour * HOUR_SIZE + period.begin.minute * HOUR_SIZE / 60;

    # end position
    end = MARGIN_LEFT + (period.end.hour if period.end.hour > 0 or period.end.minute > 0 else 24) * HOUR_SIZE + period.end.minute * HOUR_SIZE / 60
    
    # size
    size = end - begin
    
    return 'left:%s%%; width:%s%%;' % (begin, size)


@register.filter
def get_new_class_period_calendar_size(begin, duration):
    HOUR_SIZE = 4
    MARGIN_LEFT = 4
     
    # begin position
    begin = MARGIN_LEFT + begin.hour * HOUR_SIZE + begin.minute * HOUR_SIZE / 60;

    # end position
    end = begin + duration * HOUR_SIZE / 60

    # size
    size = end - begin
    
    return 'left:%s%%; width:%s%%;' % (begin, size)

@register.filter
def get_edit_period_calendar_size(period):
    HOUR_SIZE = 40
    OFFSET = 22
     
    # begin position
    begin = period.begin.hour * HOUR_SIZE + period.begin.minute * HOUR_SIZE / 60

    # end position
    end = (period.end.hour if period.end.hour > 0 or period.end.minute > 0 else 24) * HOUR_SIZE + period.end.minute * HOUR_SIZE / 60
    
    # size
    size = end - begin - OFFSET
    
    return 'left:%spx; width:%spx;' % (begin, size)


@register.filter
def get_search_period_calendar_size(period):
    HOUR_SIZE = 45
    OFFSET = 22
     
    # begin position
    begin = period.begin.hour * HOUR_SIZE + period.begin.minute * HOUR_SIZE / 60

    # end position
    end = (period.end.hour if period.end.hour > 0 or period.end.minute > 0 else 24) * HOUR_SIZE + period.end.minute * HOUR_SIZE / 60
    
    # size
    size = end - begin - OFFSET
    
    return 'left:%spx; width:%spx;' % (begin, size)

@register.filter
def get_day(user, date):
    return user.profile.get_day(date)

@register.filter
def gallery_paginator(num_photos):
    pages = (num_photos - 1) / 3 + 1
    return pages if pages > 0 else 0

@register.filter
def get_user_feedback(tutor, user):
    try:
        return tutor.reviews.get(user = user)
    except TutorReviews.DoesNotExist:
        return ''
    
@register.simple_tag
def get_universal_fee():
    return UNIVERSAL_FEE

@register.filter
def universal_fee(value):
    return value * UNIVERSAL_FEE

@register.filter
def earning_fee(value):
    return value * (1-UNIVERSAL_FEE)

@register.filter
def reviews_style(lst):
    new_list = []    

    for index in range(0, len(lst), 2):
        value1 = lst[index]
        try:
            value2 = lst[index+1]
        except IndexError:
            value2 = None
        new_list.append((value1, value2))

    return new_list

@register.simple_tag
def get_stars(rate):
    rate = int(round(rate))
    result = ''
    for i in range(5):
        star_class = 'on' if i < rate else 'off'
        result = '%s<span class="star %s"></span>' % (result, star_class)
     
    return result


@register.filter
def is_favorite(person, user):
    return user in person.profile.favorite.all()

@register.filter
def get_messages(person, user):
    messages = person.sent_messages.filter(to = user).order_by('-created')
    sent_messages = person.received_messages.filter(user = user).order_by('-created')
    
    if messages and sent_messages:
        latest = (messages[0], 'Received') if messages[0].created > sent_messages[0].created else (sent_messages[0], 'Sent')
    elif messages:
        latest = (messages[0], 'Received')
    elif sent_messages:
        latest = (sent_messages[0], 'Sent')
        
    return {
        'messages': messages,
        'unread': messages.filter(read = False).count(),
        'has_messages': bool(messages.count() or sent_messages),
        'sent_messages': sent_messages,
        'latest': latest,
     }
    
class ClassMessagesNode(template.Node):
    def __init__(self, bits):
        self.person = template.Variable(bits[1])
        self.user = template.Variable(bits[2])
        self.CLASS = template.Variable(bits[3])
        
    def render(self, context):
        person = self.person.resolve(context)
        user = self.user.resolve(context)
        CLASS = self.CLASS.resolve(context)

        messages = person.sent_messages.filter(to=user, related_class=CLASS)
        sent_messages = user.sent_messages.filter(to=person, related_class=CLASS)

        context['messages'] = messages.count()
        context['sent_messages'] = sent_messages.count()
        context['unread_messages'] = messages.filter(read=False).count()
        return ''        
    
@register.tag
def get_class_messages(parser, token):
    """
        gets the number of messages exchanged between 
        a student and a tutor in a given class
    """
    bits = token.split_contents()
    return ClassMessagesNode(bits)
    
@register.filter
def get_week(profile, date):
    return profile.get_week(date)

@register.filter
def weekclasses(profile, date=None):
    return profile.week_classes(date)
