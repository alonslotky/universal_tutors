from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import http
from django.contrib.auth.models import User

from apps.common.utils.view_utils import main_render
from apps.classes.models import *
from apps.classes.settings import *
import simplejson, datetime


@login_required
def check_status(request, class_id):
    user = request.user
    
    try:
        class_ = Class.objects.select_related().get(id = class_id)
    except Class.DoesNotExist:
        raise http.Http404()

    if class_.tutor != user and class_.student != user:
        raise http.Http404()

    start_class = class_.date
    end_class = class_.date + datetime.timedelta(minutes=class_.duration)
    
    alert_time = 5 if class_.duration < 60 else 10 
    start_alert = start_class + datetime.timedelta(minutes=alert_time)
    
    if class_.tutor == user and not class_.tutor_appeared:
        class_.tutor_appeared = True
        super(Class, class_).save()
    
    now = datetime.datetime.now()
    
    if class_.status != class_.STATUS_TYPES.BOOKED or start_class - datetime.timedelta(minutes=5) > now or end_class + datetime.timedelta(minutes=5) < now:
        return http.HttpResponse('%s' % class_.RESPONSE_TYPES.CLOSE)
    
    elif end_class < now:
        return http.HttpResponse('%s' % class_.RESPONSE_TYPES.CLOSE_ALERT)

    elif start_alert < now and start_alert + datetime.timedelta(minutes=STOP_WINDOW) > now:
        return http.HttpResponse('%s' % class_.RESPONSE_TYPES.ASK_TO_CONTINUE)
        
    return http.HttpResponse('%s' % class_.RESPONSE_TYPES.CONTINUE)


@login_required
def stop_class(request, class_id):
    user = request.user
    
    try:
        class_ = Class.objects.select_related().get(id = class_id)
    except Class.DoesNotExist:
        raise http.Http404()

    if class_.student != user:
        raise http.Http404()

    start_class = class_.date
    end_class = class_.date + datetime.timedelta(minutes=class_.duration)
    
    alert_time = 5 if class_.duration < 60 else 10 
    start_alert = start_class + datetime.timedelta(minutes=alert_time)
        
    now = datetime.datetime.now()
    
    if class_.status == class_.STATUS_TYPES.BOOKED and start_alert < now and start_alert + datetime.timedelta(minutes=STOP_WINDOW) > now:
        class_.stop_class()
        return http.HttpResponse('%s' % class_.RESPONSE_TYPES.CLOSE)
        
    return http.HttpResponse('%s' % class_.RESPONSE_TYPES.CONTINUE)



@login_required
@main_render('classes/_class_material.html')
def class_material(request, class_id):
    user = request.user
    
    try:
        class_ = Class.objects.select_related().get(id = class_id)
    except Class.DoesNotExist:
        raise http.Http404()

    if class_.tutor != user and class_.student != user:
        raise http.Http404()

    material = class_.get_material()
    recordings = class_.get_recordings()
        
    return {
        'class': class_,
        'material': material,
        'recordings': recordings,
    }


@main_render('classes/fragments/_option_items.html')
def system_levels_options(request, system_id, all_option):
    all_option = int(all_option)
    
    try:
        system = EducationalSystem.objects.get(id = system_id)
        items = system.levels.all()
    except EducationalSystem.DoesNotExist:
        items = ClassLevel.objects.all()
    
    return {
        'items': items,
        'blank': {
            'value': '',
            'description': 'Any level' if all_option else '-------',
        },
    }

@main_render('classes/fragments/_option_items.html')
def system_subjects_options(request, system_id, all_option):
    all_option = int(all_option)
    
    try:
        system = EducationalSystem.objects.get(id = system_id)
        items = system.subjects.all()
    except EducationalSystem.DoesNotExist:
        items = ClassSubject.objects.all()
    
    return {
        'items': items,
        'blank': {
            'value': '',
            'description': 'Any subject' if all_option else '-------',
        },
    }


@main_render('classes/fragments/_option_items.html')
def subject_systems_options(request, subject_id, all_option):
    all_option = int(all_option)
    
    try:
        subject = ClassSubject.objects.get(id = subject_id)
        items = subject.systems.all()
    except ClassSubject.DoesNotExist:
        items = EducationalSystem.objects.all()
    
    return {
        'items': items,
        'blank': {
            'value': '',
            'description': 'Any system' if all_option else '-------',
        },
    }
