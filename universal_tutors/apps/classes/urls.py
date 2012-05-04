from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib import admin

# Main
urlpatterns = patterns('apps.classes.views.main',
    url(r'^(?i)detail/$', 'detail', {}, name = "class_detail"),
    url(r'^(?i)detail/(?P<class_id>\d+)/$', 'detail', {}, name = "class_detail"),
    url(r'^(?i)download/(?P<class_id>\d+)/$', 'download', {}, name = "class_download"),
)






