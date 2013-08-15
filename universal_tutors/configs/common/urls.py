from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import os
####Checking out avatar##########
#import allauth
#from  avatar import *
#import avatar

handler500 = 'apps.common.views.server_error'
admin.autodiscover()

try:
    from filebrowser.sites import site
except:
    pass

# Internal app patterns
urlpatterns = patterns('',
    url(r'^', include('apps.common.urls')),
    url(r'^', include('apps.core.urls')),
    url(r'^', include('apps.profile.urls')),
    url(r'^(?i)faq/', include('apps.faq.urls')),
    url(r'^(?i)classes/', include('apps.classes.urls')),
)

# Admin patterns
urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^admin_tools/', include('admin_tools.urls')),
	url(r'^grappelli/', include('grappelli.urls')),
)

try:
    urlpatterns += patterns('',
        (r'^admin/filebrowser/', include(site.urls)),
    )
except:
    urlpatterns += patterns('',
        (r'^admin/filebrowser/', include('filebrowser.urls')),
    )

# Site media patterns
urlpatterns += patterns('',
    (r'^favicon\.ico$', redirect_to, {'url': '/static/img/favicon.ico'}),
    (r'^apple\-touch\-icon\.png$', redirect_to, {'url': '/static/img/apple-touch-icon.png'}),
    (r'^robots\.txt$', redirect_to, {'url': '/static/robots.txt'}),
	(r'^tinymce/', include('tinymce.urls')),
	(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
	(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages':'django.conf'}),
)

if settings.DEBUG:
    urlpatterns+= patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        }),
        (r'^cache-forever/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
        (r'^500/$', 'apps.common.views.server_error'),
    )

# Pluggable apps
urlpatterns += patterns('',
    url(r'^accounts/social/connections/$', redirect_to, {'url': '/dashboard/edit_profile/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)

# PAYPAL
urlpatterns += patterns('',
    (r'^topupcredits/paypal/ipn/universaltutors/', include('paypal.standard.ipn.urls')),
)

#urlpatterns = patterns('',
    # ...
#    (r'^avatar/', include('avatar.urls')),
#)

urlpatterns += staticfiles_urlpatterns()



