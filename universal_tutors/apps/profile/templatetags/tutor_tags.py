from django import template
from django.contrib.auth.models import User
register = template.Library()

from apps.profile.models import TutorReview
from apps.classes.settings import *

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
    
    return {
        'messages': messages,
        'unread': messages.filter(read = False).count(),
     }
    
@register.filter
def get_week(profile, date):
    return profile.get_week(date)
