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
from apps.classes.models import *
from apps.core.models import Video

import datetime, random

@main_render(template='core/home.html')
def home(request):
    user = request.user

    featured_tutors = Tutor.objects.select_related().filter(profile__featured=True).order_by('-profile__activation_date')
    no_featured_tutors = featured_tutors.count()

    try:
        video = Video.objects.filter(type=Video.VIDEO_TYPES.HOME, active=True).latest('id')
    except Video.DoesNotExist:
        video = None

    return {
        'featured_tutors': random.sample(featured_tutors, 3) if no_featured_tutors > 3 else random.sample(featured_tutors, no_featured_tutors),
        'video': video,
    }

        

@main_render(template='core/search.html')
def search(request):
    user = request.user
    tutors = None
    
    subjects = set()
    levels = set()
    
    query = request.GET.get('text', '')
    what = request.GET.get('what', None)
    
    system = request.GET.get('system', '')
    subject = request.GET.get('subject', '')
    level = request.GET.get('level', '')

    price = int(request.GET.get('price', 0))
    day = int(request.GET.get('day', -1))
    time = int(request.GET.get('time', -1))
    crb = request.GET.get('crb', False)
    sort = request.GET.get('sort', 'price')
    
    results_per_page = request.GET.get('results_per_page', 10)
    
    tutors = Tutor.objects.select_related()    
    
    today = datetime.date.today()
    
    if crb:
        tutors = tutors.filter(profile__crb_expiry_date__gte=today)
    
    if query:
        if what == 'tutor':
            words = query.split()
            for word in words:
                tutors = tutors.filter(Q(first_name__icontains=word) | Q(last_name__icontains=word) | Q(username__icontains=word))
        elif what == 'subject':
            tutors = tutors.filter(subjects__subject__subject__icontains=query)
        elif what == 'level':
            tutors = tutors.filter(subjects__level__level__icontains=query)


    if system:
        tutors = tutors.filter(subjects__system__id = system)

    if subject:
        tutors = tutors.filter(subjects__subject__id = subject)

    if level:
        tutors = tutors.filter(subjects__level__id = level)

    
    if price:
        tutors = tutors.filter(Q(subjects__credits__lte=price))
    
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
    
    if system:
        try:
            selected_system = EducationalSystem.objects.get(id = system)
        except EducationalSystem.DoesNotExist:
            selected_system = None
    else:
        selected_system = None
          
    return { 
        'systems': EducationalSystem.objects.all(),
        'subjects': ClassSubject.objects.all(),
        'levels': ClassLevel.objects.all(),
        'selected_system': selected_system,
        'results_per_page': results_per_page,
        'user': user,
        'tutors': tutors.distinct(),
    }
