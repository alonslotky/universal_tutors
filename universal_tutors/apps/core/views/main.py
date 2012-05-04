from django import http
from django.conf import settings
from django.http import  HttpResponseServerError
from django.db.models import Q, Sum
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.common.utils.view_utils import main_render
from apps.profile.models import UserProfile, WeekAvailability
from universal_tutors.apps.classes.models import ClassSubject

import datetime

@main_render(template='core/home.html')
def home(request):
    user = request.user

    return {}

def _get_simple_results(data):
    q = data.get('text', None)
    what = data.get('what')
    sort = data.get('sort', None)
    price = data.get('price', None)
    day = data.get('day', None)
    time = data.get('time', None)
    
    tutors = None
    if q:
        tutors = User.objects.select_related().filter(profile__type=UserProfile.TYPES.TUTOR)
        if what == 'tutors':
            tutors = tutors.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
    
        elif what == 'subjects':
            subjects = ClassSubject.objects.all()
            subjects = subjects.filter(subject__icontains=q)
            tutors = tutors.filter(classes_as_tutor__in=subjects)
        if sort:
            if sort == 'price':
                tutors = tutors.order_by('profile__max_credits')
            elif sort == 'rating':
                tutors = tutors.order_by('-profile__avg_rate')
            elif sort == 'classes':
                tutors = tutors.order_by('-profile__classes_given')
                
        if price:

            price = int(price)
            if price == 1:
                tutors = tutors.filter(profile__max_credits__lt=5)
            elif price == 2:
                tutors = tutors.filter(profile__max_credits__gte=5, profile__max_credits__lt=10)
            elif price == 3:
                tutors = tutors.filter(profile__max_credits__gte=10, profile__max_credits__lt=15)
            elif price == 4:
                tutors = tutors.filter(profile__max_credits__gte=15, profile__max_credits__lt=20)
            elif price == 5:
                tutors = tutors.filter(profile__max_credits__gte=20, profile__max_credits__lt=25)
            elif price == 6:
                tutors = tutors.filter(profile__max_credits__gte=25, profile__max_credits__lt=30)
            elif price == 7:
                tutors = tutors.filter(profile__max_credits__gte=30)
                
            
        if time:
            weekdays = WeekAvailability.objects.filter(user__in=tutors)
            if day:
                weekdays = weekdays.filter(weekday=int(day))
            t = datetime.time(int(time), 0)
            weekdays = weekdays.filter(begin=t)
            tutors = tutors.filter(id__in=[i.user.id for i in weekdays])
        elif day:
            tutors = tutors.filter(week_availability__weekday=int(day))
            
    return tutors
        

@main_render(template='core/search.html')
def search(request):
    tutors = None

    if request.GET:
        search_type = request.GET.get('search')
        tutors = _get_simple_results(request.GET)

    query = ''
    query_type = ''
    # tutors = User.objects.select_related().filter(profile__type = UserProfile.TYPES.TUTOR)
    
    return { 
        'tutors': tutors,
        'query': query,
        'query_type': query_type,
    }
