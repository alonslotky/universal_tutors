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
    url(r'^(?i)reports/students/download/$', 'reports_students', {'xls':1},name='reports_students_download'),
    url(r'^(?i)reports/tutors/$', 'reports_tutors', name='reports_tutors'),
    url(r'^(?i)reports/tutors/download/$', 'reports_tutors', {'xls':1}, name='reports_tutors_download'),
    url(r'^(?i)reports/classes/$', 'reports_classes', name='reports_classes'),
    url(r'^(?i)reports/classes/download/$', 'reports_classes', {'xls':1}, name='reports_classes_download'),
    url(r'^(?i)reports/financial/$', 'reports_financial', name='reports_financial'),
    url(r'^(?i)reports/financial/download/$', 'reports_financial', {'xls':1}, name='reports_financial_download'),

    url(r'^(?i)monitoring/$', 'monitoring_classes', name='monitoring_classes'),
    url(r'^(?i)monitoring/(?P<class_id>\d+)/$', 'monitoring_class', name='monitoring_class'),

    url(r'^(?i)waiting_for_approval/$', 'waiting_approval', name='waiting_approval'),
)

# Ajax
urlpatterns += patterns('apps.core.views.ajax',
    url(r'^(?i)waiting_for_approval/approve_item/$', 'approve_item', name='approve_item'),
    url(r'^(?i)waiting_for_approval/approve_item/(?P<tutor_id>\d+)/(?P<type>\w+)/(?P<approve>\d+)/$', 'approve_item', name='approve_item'),

    url(r'^(?i)timezones/$', 'timezones', name='get_timezones'),
    url(r'^(?i)timezones/(?P<country>\w+)/$', 'timezones', name='get_timezones'),

    url(r'^(?i)formassembly/submit/$', 'formassembly_submit', name='formassembly_submit'),
)