from django import http
from django.conf import settings
from django.http import  HttpResponseServerError
from django.db.models import Q, Sum
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.common.utils.view_utils import main_render
from apps.profile.models import UserProfile

import datetime

@main_render(template='core/home.html')
def home(request):
    user = request.user

    return {}

@main_render(template='core/search.html')
def search(request):

    tutors = User.objects.select_related().filter(type = UserProfile.TYPES.TUTOR)
    
    return { 
        'tutors': tutors,
    }
