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
    url(r'^(?i)search/$', 'search', name='search'),

    url(r'^(?i)reports/$', 'reports', name='reports'),
    url(r'^(?i)reports/students/$', 'reports_students', name='reports_students'),
    url(r'^(?i)reports/tutors/$', 'reports_tutors', name='reports_tutors'),
    url(r'^(?i)reports/classes/$', 'reports_classes', name='reports_classes'),
    url(r'^(?i)reports/financial/$', 'reports_financial', name='reports_financial'),

    url(r'^(?i)monitoring/$', 'monitoring_classes', name='monitoring_classes'),
    url(r'^(?i)monitoring/(?P<class_id>\d+)/$', 'monitoring_class', name='monitoring_class'),
)

# Ajax
urlpatterns += patterns('apps.core.views.ajax',
    
)