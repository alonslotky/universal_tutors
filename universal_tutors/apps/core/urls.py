from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

import os
import views
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib import admin

#to be used when using different templates for the tutors signupwizard!
from apps.profile.views.login import TutorSignupWizard, TUTOR_SIGNUP_FORMS
from apps.profile.forms import MultiPartSignupFormStep1, MultiPartSignupFormStep2, MultiPartSignupFormStep3, MultiPartSignupFormStep4, \
                       MultiPartSignupFormStep5, MultiPartSignupFormStep6

#to be used when using different templates for the tutors signupwizard!
from apps.profile.views.login import TutorSignupWizard, TUTOR_SIGNUP_FORMS
from apps.profile.forms import MultiPartSignupFormStep1, MultiPartSignupFormStep2, MultiPartSignupFormStep3, MultiPartSignupFormStep4, \
                       MultiPartSignupFormStep5, MultiPartSignupFormStep6

#example
tutor_forms = (
    ('contactdata', MultiPartSignupFormStep1),
    ('leavemessage', MultiPartSignupFormStep2),
)

contact_wizard = TutorSignupWizard.as_view(tutor_forms,)
    #url_name='contact_step', done_step_name='finished')

urlpatterns = patterns('apps.profile.views.login',
    url(r'^contact/(?P<step>.+)/$', contact_wizard, name='contact_step'),
    url(r'^contact/$', contact_wizard, name='contact'),
  )

#recreating example
named_tutor_forms = (
    ('step1', MultiPartSignupFormStep1),
    ('step2', MultiPartSignupFormStep2),
    ('step3', MultiPartSignupFormStep3),
    ('step4', MultiPartSignupFormStep4),
    ('step5', MultiPartSignupFormStep5),
)

#tutor_wizard = TutorSignupWizard.as_view(named_tutor_forms,
    #url_name='step11', done_step_name='finished')

urlpatterns = patterns('apps.profile.views.login',
    #url(r'^account/signup/tutor/(?P<step>.+)/$', tutor_wizard,name='step11'),
    #url(r'^account/signup/tutor/$', tutor_wizard),
)

# Registration/Login views
urlpatterns = patterns('apps.profile.views.login',
    #url(r"^(?i)account/signup/tutor/$", 'tutor_signup',  name="tutor_signup"),
    #url(r"^(?i)account/signup/tutorsubjects/$", 'tutor_signup1',  name="tutor_signup1"),
    url(r'^$', TutorSignupWizard.as_view(TUTOR_SIGNUP_FORMS), name="tutor_signup"),
    #url(r'^$account/signup/tutor/', TutorSignupWizard.as_view(TUTOR_SIGNUP_FORMS), name="tutor_signup"),
    #url(r'^account/signup/tutor2/$', TutorSignupWizard.as_view(TUTOR_SIGNUP_FORMS), name="tutor_signup2"),
)
# Main
urlpatterns = patterns('apps.core.views.main',
    #url(r'^$', 'home', name='home'),
    url(r'^$', TutorSignupWizard.as_view(TUTOR_SIGNUP_FORMS), name="home"),
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

    url(r'^(?i)withdraws/manual/$', 'withdraws_manual', name='withdraws_manual'),
    url(r'^(?i)withdraws/manual/payment/(?P<withdraw_id>\d+)/$', 'withdraws_manual_payment', name='withdraws_manual_payment'),
    url(r'^(?i)withdraws/monthly/$', 'withdraws_monthly', name='withdraws_monthly'),
    url(r'^(?i)withdraws/monthly/payment/(?P<currency_acronym>\w+)/$', 'withdraws_monthly_payment', name='withdraws_monthly_payment'),

)

# Ajax
urlpatterns += patterns('apps.core.views.ajax',
    url(r'^(?i)waiting_for_approval/approve_item/$', 'approve_item', name='approve_item'),
    url(r'^(?i)waiting_for_approval/approve_item/(?P<tutor_id>\d+)/(?P<type>\w+)/(?P<approve>\d+)/$', 'approve_item', name='approve_item'),

    url(r'^(?i)timezones/$', 'timezones', name='get_timezones'),
    url(r'^(?i)timezones/(?P<country>\w+)/$', 'timezones', name='get_timezones'),

    url(r'^(?i)formassembly/submit/$', 'formassembly_submit', name='formassembly_submit'),
)