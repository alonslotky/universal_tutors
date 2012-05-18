from django import http
from django.conf import settings
from django.http import  HttpResponseServerError
from django.db.models import Q, Sum, Max
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.common.utils.view_utils import main_render
from apps.profile.models import UserProfile, WeekAvailability, Tutor
from apps.classes.models import ClassSubject
from apps.core.models import Video

import datetime, random

@main_render(template='core/home.html')
def home(request):
    user = request.user

    featured_tutors = Tutor.objects.select_related().filter(profile__featured=True).order_by('-profile__activation_date')
    no_featured_tutors = featured_tutors.count()

    try:
        video = Video.objects.filter(active=True).latest('id')
    except Video.DoesNotExist:
        video = None

    return {
        'featured_tutors': random.sample(featured_tutors, 3) if no_featured_tutors > 3 else random.sample(featured_tutors, no_featured_tutors),
        'video': video,
    }

        

@main_render(template='core/search.html')
def search(request):
    tutors = None
    
    subjects = set()
    levels = set()
    
    for sub in ClassSubject.objects.all():
        splited_sub = sub.subject.split(',')
        try:
            subjects.add(splited_sub[0].strip())
        except IndexError:
            pass

        try:
            levels.add(splited_sub[1].strip())
        except IndexError:
            pass        

    query = request.GET.get('text', '')
    what = request.GET.get('what', None)
    
    system = request.GET.get('system', None)
    subject = request.GET.get('subject', '')
    level = request.GET.get('level', '')

    price = int(request.GET.get('price', 0))
    day = int(request.GET.get('day', -1))
    time = int(request.GET.get('time', -1))
    crb = request.GET.get('crb', False)
    sort = request.GET.get('crb', 'price')
    
    tutors = Tutor.objects.select_related()    
    
    if crb:
        tutors = tutors.filter(profile__crb_checked=True)
    
    if query:
        if what == 'tutors':
            tutors = tutors.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query))
        else :
            tutors = tutors.filter(subjects__subject__subject__icontains=query)

    if price:
        tutors = tutors.filter(Q(subjects__subject__subject__icontains=subject), Q(subjects__subject__subject__icontains=level), Q(subjects__credits__lte=price))
    else:
        tutors = tutors.filter(Q(subjects__subject__subject__icontains=subject), Q(subjects__subject__subject__icontains=level))
    
    
    if day >= 0 and time >=0:
        tutors = tutors.filter(week_availability__weekday=day, week_availability__begin__lte=datetime.time(time,0), week_availability__end__gte=datetime.time(time,0))
    else:
        if day >= 0:
            tutors = tutors.filter(week_availability__weekday=day)    
        if time >= 0:
            tutors = tutors.filter(week_availability__begin=datetime.time(time,0))

    if sort == 'price':
        tutors = tutors.annotate(price = Max('subjects__credits')).order_by('price')
    elif sort == 'rating':
        tutors = tutors.distinct().order_by('-profile__avg_rate')
    elif sort == 'classes':
        tutors = tutors.distinct().order_by('-profile__classes_given')
            
    return { 
        'subjects': sorted(subjects),
        'levels': sorted(levels),
        
        'tutors': tutors.distinct(),
    }
