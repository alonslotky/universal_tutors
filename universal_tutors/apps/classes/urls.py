from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib import admin
from fancy_autocomplete.views import AutocompleteSite, LabeledAutocomplete, ObjectAutocomplete

from apps.classes.models import ClassSubject


class SubjectsAutocomplete(LabeledAutocomplete):
    """
    Subjects for autocomplete
    """
    queryset = ClassSubject.objects.all().distinct()

    lookup = 'icontains'
    search_fields = ('subject',)
    limit = 10

# Main
urlpatterns = patterns('apps.classes.views.main',
    url(r'^(?i)detail/$', 'detail', {}, name = "class_detail"),
    url(r'^(?i)detail/(?P<class_id>\d+)/$', 'detail', {}, name = "class_detail"),
    url(r'^(?i)download/(?P<class_id>\d+)/$', 'download', {}, name = "class_download"),
)

urlpatterns += patterns('apps.classes.views.ajax',
    url(r'^(?i)check_status/(?P<class_id>\d+)/$', 'check_status', {}, name = "check_status"),
    url(r'^(?i)stop_class/(?P<class_id>\d+)/$', 'stop_class', {}, name = "stop_class"),
    url(r'^autocomplete/subjects/$', SubjectsAutocomplete.as_view(), name='autocomplete_subjects'),
)





