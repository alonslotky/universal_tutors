from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

import os
import views

# Main
urlpatterns = patterns('apps.core.views.main',
    url(r'^$', 'home', name='home'),
    #url(r'^(?i)search/$', 'search', name='search'),
)

# Ajax
urlpatterns += patterns('apps.core.views.ajax',
    
)