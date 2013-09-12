from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

import os
import views

import autocomplete_light
autocomplete_light.autodiscover()
admin.autodiscover()

# AJAX Helper patterns
urlpatterns = patterns('apps.common.utils.view_utils',
	url(r'^ajax-view/(?P<view_name>[\w-]+)/$', "ajax_view", {}, name="ajax_view"),
)

# Shared Pluggable URLS
urlpatterns += patterns('apps.common.views',
	url(r'^contact-us/$', 'contact_us', name='contact_us'),
)

urlpatterns += patterns('apps.common.views.ajax',
    # url(r'^contact/$', 'contact', name='contact'),
)