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
from apps.classes.settings import CLASS_LANGUAGES
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
    recordings = None
    template = 'classes/detail.html'
    
    try:
        class_ = Class.objects.select_related().get(id = class_id)
    except Class.DoesNotExist:
        raise http.Http404()

    if class_.tutor != user and class_.student != user:
        raise http.Http404()

    now = datetime.datetime.now()

    start = now + datetime.timedelta(minutes = 5)
    end = now - datetime.timedelta(minutes = class_.duration + 5)
    
    if class_.date > start:
        before = True
    
    elif class_.date < end or (class_.status != class_.STATUS_TYPES.BOOKED):
        after = True
        material = class_.get_material()
        recordings = class_.get_recordings()
        
    if not before and not after:
        template = 'classes/class.html'
    
    return {
        'TEMPLATE': template,
        'class': class_,
        'profile': profile,
        'before': before,
        'after': after,
        'material': material,
        'recordings': recordings,
        'CLASS_LANGUAGES': CLASS_LANGUAGES,
    }

@login_required
@main_render('classes/no_flash.html')
def no_flash(request, class_id):
    """
    detailed profile from a user
    """
    user = request.user
    profile = user.profile

    try:
        class_ = Class.objects.select_related().get(id = class_id)
    except Class.DoesNotExist:
        raise http.Http404()

    if class_.tutor != user and class_.student != user:
        raise http.Http404()

    return {
        'class': class_,
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


