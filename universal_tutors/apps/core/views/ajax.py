from django import http
from django.conf import settings
from django.http import  HttpResponseServerError
from django.db.models import Q, Sum
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.common.utils.view_utils import main_render
from apps.profile.models import *

import datetime

def approve_item(request, tutor_id, type, approve):
    user = request.user
    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()
    
    approve = int(approve)
    try:
        tutor = User.objects.select_related().get(id = tutor_id, profile__type=UserProfile.TYPES.TUTOR)
        profile = tutor.profile
    except Class.DoesNotExist:
        raise http.Http404()
    
    if type == 'image':
        profile.profile_image_approved = bool(approve)
    if type == 'description':
        profile.about_approved = bool(approve)
    if type == 'video':
        profile.video_approved = bool(approve)
    if type == 'qualifications':
        profile.qualification_documents_approved = bool(approve)
    if type == 'crb':
        if approve:
            date = request.GET.get('crb_date', '').split('-')
            try:
                profile.crb_expiry_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            except:
                return http.HttpResponse('approved' if profile.crb_checked else 'not approved')
        else:
            profile.crb_expiry_date = None
    
    profile.save()
    
    return http.HttpResponse('approved' if approve else 'not approved')


    
    
    return {
        'months': months,
        'today': datetime.date.today(),
        'next_month': nxt_month,
        'prev_month': prv_month,
    }