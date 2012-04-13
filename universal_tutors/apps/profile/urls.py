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
    url(r'^(?i)profile/$', 'profile', {}, name = "profile"),
    url(r'^(?i)profile/(?P<username>[\w\-\_]+)/$', 'profile', {}, name = "profile"),
)

# Profile management
urlpatterns += patterns('apps.profile.views.main',
#    url(r'^signup/complete/$', 'register_complete', {}, name = "register_complete"),
    url(r'^(?i)dashboard/$', 'dashboard', {}, name = "dashboard"),
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
