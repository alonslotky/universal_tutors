from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from django.conf import settings

from apps.common.utils.view_utils import main_render
from apps.common.utils.decorators import over16_required

from apps.classes.models import Class
import datetime


@login_required
@main_render()
def detail(request, class_id):
    """
    detailed profile from a user
    """
    user = request.user
    profile = user.profile

    before = False
    after = False
    material = None
    template = 'classes/detail.html'
    
    try:
        class_ = Class.objects.select_related().get(id = class_id)
    except Class.DoesNotExist:
        raise http.Http404()

    if class_.tutor != user and class_.student != user:
        raise http.Http404()

    now = datetime.datetime.now()

    start = now + datetime.timedelta(minutes=5)
    start_date = start.date()
    start_time = start.time()
    
    end = now - datetime.timedelta(minutes=5)
    end_date = end.date()
    end_time = end.time()
    
    if class_.date > start_date or (class_.date == start_date and class_.start > start_time):
        before = True
    
    elif class_.date < end_date or (class_.date == end_date and class_.end < end_time):
        after = True
        material = class_.get_material()
        
    if not before and not after:
        template = 'classes/class.html'
    
    return {
        'TEMPLATE': template,
        'class': class_,
        'profile': profile,
        'before': before,
        'after': after,
        'material': material,
    }


@login_required
@main_render()
def download(request, class_id):
    """
    detailed profile from a user
    """
    user = request.user
    profile = user.profile

    try:
        class_ = Class.objects.select_related().get(id = class_id)
    except Class.DoesNotExist:
        raise http.Http404()

    if class_.tutor != user and class_.student != user and class_.student.parent != user:
        raise http.Http404()

    return http.HttpResponseRedirect(class_.download(request.GET.get('id')))


