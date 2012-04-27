from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib import admin

# Registration/Login views
urlpatterns = patterns('apps.profile.views.login',
    url(r"^(?i)account/signup/$", 'signup',  name="signup"),
    url(r"^(?i)account/signin/$", 'signin', name="login"),
    url(r"^(?i)account/logout/$", 'logout_view', name="logout"),
)

# Front-end profile
urlpatterns += patterns('apps.profile.views.main',
    url(r"^(?i)dashboard/$", 'dashboard', name="dashboard"),
    url(r'^(?i)profile/$', 'profile', {}, name = "profile"),
    url(r'^(?i)profile/(?P<username>[\w\-\_]+)/$', 'profile', {}, name = "profile"),
    url(r'^(?i)edit_tutor_profile/$', 'edit_tutor_profile', {}, name = "edit_tutor_profile"),
)

# Tutors
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)tutor/classes/$', 'tutor_classes', {}, name = "tutor_classes"),
    url(r'^(?i)tutor/messages/$', 'tutor_messages', {}, name = "tutor_messages"),
)

urlpatterns += patterns('apps.profile.views.ajax',
    url(r'^(?i)edit_week_period/$', 'edit_week_period', {}, name = "user_edit_week_period"),
    url(r'^(?i)edit_week_period/(?P<period_id>\d+)/(?P<begin>[\d\-]+)/(?P<end>[\d\-]+)/(?P<weekday>\d)/$', 'edit_week_period', {}, name = "user_edit_week_period"),
    url(r'^(?i)delete_week_period/(?P<period_id>\d+)/$', 'delete_week_period', {}, name = "user_delete_week_period"),
    url(r'^(?i)view_week_period/$', 'view_week_period', {}, name = "user_edit_view_week_period"),

    url(r'^(?i)view_week_period/(?P<date>[\d\-]+)/$', 'view_week_period', {}, name = "user_edit_view_week_period"),
    url(r'^(?i)edit_this_week_period/(?P<date>[\d\-]+)/$', 'edit_this_week_period', {}, name = "user_edit_this_week_period"),
    url(r'^(?i)edit_this_week_period/(?P<date>[\d\-]+)/(?P<type>\d+)/(?P<period_id>\d+)/(?P<begin>[\d\-]+)/(?P<end>[\d\-]+)/(?P<weekday>\d)/$', 'edit_this_week_period', {}, name = "user_edit_this_week_period"),
    url(r'^(?i)delete_this_week_period/(?P<period_id>\d+)/$', 'delete_this_week_period', {}, name = "user_delete_this_week_period"),
)

# Students
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)student/classes/$', 'student_classes', {}, name = "student_classes"),
    url(r'^(?i)student/messages/$', 'student_messages', {}, name = "student_messages"),
)

urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)newsletter_verify_email_address/(?P<key>[\w\-\_]+)/$', 'newsletter_verify_email_address', {}, name = "newsletter_verify_email_address"),
#   url(r'^(?i)newsletter_verify_email_address/(?P<key>[\W\d]+)/$', 'newsletter_verify_email_address', {}, name = "newsletter_verify_email_address"),
)

# Ajax views
urlpatterns += patterns('apps.profile.views.ajax',
    url(r'^(?i)add_newsletter_subscription/$', 'add_newsletter_subscription', name = "add_newsletter_subscription"),
    url(r'^(?i)change_photo/$', 'change_photo', name = "change_photo"),
)






