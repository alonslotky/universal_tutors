from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings

from apps.common.utils.view_utils import main_render
from apps.common.utils.decorators import over16_required

from apps.classes.models import Class

@login_required
@main_render('classes/detail.html')
def detail(request, class_id):
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

    return {
        'class': class_,
        'profile': profile,
    }

