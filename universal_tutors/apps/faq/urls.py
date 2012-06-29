from django.conf.urls.defaults import *

# Main
urlpatterns = patterns('apps.faq.views',
    url(r'^$', 'faq', name='faq'),
)
