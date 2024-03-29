from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib import admin

#to be used when using different templates for the tutors signupwizard!
from apps.profile.views.login import TutorSignupWizard, TUTOR_SIGNUP_FORMS
from apps.profile.forms import MultiPartSignupFormStep1, MultiPartSignupFormStep2, MultiPartSignupFormStep3, MultiPartSignupFormStep4, \
                       MultiPartSignupFormStep5, MultiPartSignupFormStep6

# Registration/Login views
urlpatterns = patterns('apps.profile.views.login',
    #url(r"^(?i)account/signup/tutor/$", 'tutor_signup',  name="tutor_signup"),
    url(r"^(?i)account/signup/tutorsubjects/$", 'tutor_signup1',  name="tutor_signup1"),
    url(r'^account/signup/tutor/$', TutorSignupWizard.as_view(TUTOR_SIGNUP_FORMS), name="tutor_signup"),
    url(r'^account/signup/tutor2/$', TutorSignupWizard.as_view(TUTOR_SIGNUP_FORMS), name="tutor_signup2"),
    # url(r'^account/signup/tutor/$', TutorSignupWizard(TUTOR_SIGNUP_FORMS), name="tutor_signup"),

#    (r'^account/signup/tutor2/$', TutorSignupWizard.as_view([MultiPartSignupFormStep1, MultiPartSignupFormStep2, \
#                                                             MultiPartSignupFormStep3, MultiPartSignupFormStep4, \
#                                                             MultiPartSignupFormStep5, MultiPartSignupFormStep6])),    
    url(r"^(?i)account/signup/student/$", 'student_signup',  name="student_signup"),
    url(r"^(?i)account/signup/parent/$", 'parent_signup',  name="parent_signup"),
    url(r"^(?i)account/signup/$", 'signup',  name="signup"),
    url(r"^(?i)account/signin/$", 'signin', name="login"),
    url(r"^(?i)account/logout/$", 'logout_view', name="logout"),
    url(r"^(?i)account/successfull/signup/$", 'successfull_signup', name="successfull_signup"),
    url(r"^(?i)accounts/social/signup/$", 'social_signup', name="socialaccount_signup"),
    url(r'^(?i)accounts/genres/$', 'show_genres',name='show_genres'),
    url(r'^(?i)accounts/tutor5/$', 'show_genres',name='show_genres'),
    )

# Front-end profile
urlpatterns += patterns('apps.profile.views.main',
    url(r"^(?i)dashboard/$", 'edit_profile', name="dashboard"),
    url(r'^(?i)profile/$', 'profile', {}, name = "profile"),
    url(r'^(?i)profile/(?P<username>[\w.@+-]+)/$', 'profile', {}, name = "profile"),
    url(r'^(?i)edit_profile/$', 'edit_profile', {}, name = "edit_profile"),

    url(r'^(?i)tutor/profile/edit/$', 'edit_tutor_profile', {}, name = "edit_tutor_profile"),
    url(r'^(?i)student/profile/edit/$', 'edit_student_profile', {}, name = "edit_student_profile"),
    url(r'^(?i)parent/profile/edit/$', 'edit_parent_profile', {}, name = "edit_parent_profile"),

    url(r'^(?i)history/$', 'history', {}, name = "history"),
    url(r'^(?i)history/(?P<username>[\w.@+-]+)/$', 'history', {}, name = "history"),
)

# Tutors
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)tutor/classes/$', 'tutor_classes', {}, name = "tutor_classes"),
    url(r'^(?i)tutor/messages/$', 'tutor_messages', {}, name = "tutor_messages"),
    url(r'^(?i)tutor/crb_form/$', 'crb_form', {}, name = "crb_form"),

    url(r'^(?i)book-class/(?P<username>[\w.@+-]+)/$', 'book_class', {}, name = "book_class"),
    url(r'^(?i)report/(?P<username>[\w.@+-]+)/$', 'report', {}, name = "report"),
    
    url(r'^(?i)tutor/test/class/$', 'test_class', {}, name = "tutor_test_class"),
)

urlpatterns += patterns('apps.profile.views.ajax',
    url(r'^(?i)edit_week_period_signup/$', 'edit_week_period_signup', {}, name = "edit_week_period_signup"),
    url(r'^(?i)edit_week_period_signup/(?P<period_id>\d+)/(?P<begin>[\d\-]+)/(?P<end>[\d\-]+)/(?P<weekday>\d)/$', 'edit_week_period_signup', {}, name = "edit_week_period_signup"), 
    #url(r'^(?i)delete_week_period_signup/$', 'delete_week_period_signup', {}, name = "delete_week_period_signup"),
    #url(r'^(?i)delete_week_period_signup/(?P<period_id>\d+)/$', 'delete_week_period_signup', {}, name = "delete_week_period_signup"),
    
    
    url(r'^(?i)edit_week_period/$', 'edit_week_period', {}, name = "user_edit_week_period"),
    url(r'^(?i)edit_week_period/(?P<period_id>\d+)/(?P<begin>[\d\-]+)/(?P<end>[\d\-]+)/(?P<weekday>\d)/$', 'edit_week_period', {}, name = "user_edit_week_period"),
    url(r'^(?i)delete_week_period/$', 'delete_week_period', {}, name = "user_delete_week_period"),
    url(r'^(?i)delete_week_period/(?P<period_id>\d+)/$', 'delete_week_period', {}, name = "user_delete_week_period"),
    url(r'^(?i)view_week_period/$', 'view_week_period', {}, name = "user_edit_view_week_period"),

    url(r'^(?i)view_week_period/(?P<date>[\d\-]+)/$', 'view_week_period', {}, name = "user_edit_view_week_period"),
    url(r'^(?i)edit_this_week_period/(?P<date>[\d\-]+)/$', 'edit_this_week_period', {}, name = "user_edit_this_week_period"),
    url(r'^(?i)edit_this_week_period/(?P<date>[\d\-]+)/(?P<type>\d+)/(?P<period_id>\d+)/(?P<begin>[\d\-]+)/(?P<end>[\d\-]+)/(?P<weekday>\d)/$', 'edit_this_week_period', {}, name = "user_edit_this_week_period"),
    url(r'^(?i)delete_this_week_period/(?P<period_id>\d+)/$', 'delete_this_week_period', {}, name = "user_delete_this_week_period"),

    url(r'^(?i)tutor/cancel_class/$', 'tutor_cancel_class', {}, name = "tutor_cancel_class"),
    url(r'^(?i)tutor/rate_student/$', 'tutor_rate_student', {}, name = "tutor_rate_student"),
    
    url(r'^(?i)tutor/favorite/$', 'favorite', {}, name = "favorite"),
    url(r'^(?i)tutor/favorite/(?P<person_id>\d+)/$', 'favorite', {}, name = "favorite"),

    url(r'^(?i)tutor/accept_class/$', 'accept_class', {}, name = "tutor_accept_class"),
    url(r'^(?i)tutor/accept_class/(?P<class_id>\d+)/$', 'accept_class', {}, name = "tutor_accept_class"),
    url(r'^(?i)tutor/reject_class/$', 'reject_class', {}, name = "tutor_reject_class"),

    url(r'^(?i)confirm-book-class/(?P<tutor_id>\d+)/$', 'book_class', {}, name = "confirm_book_class"),
 
    url(r'^(?i)ajax-book-class/(?P<username>[\w.@+-]+)/$', 'ajax_book_class', {}, name = "ajax_book_class"),
    url(r'^(?i)ajax-book-class/(?P<username>[\w.@+-]+)/(?P<date>[\d\-]+)/$', 'ajax_book_class', {}, name = "ajax_book_class"),

    url(r'^(?i)test_class/status/$', 'check_tutor_class_status', {}, name = "check_tutor_class_status"),
)

# parents
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)parent/messages/$', 'parent_messages', {}, name = "parent_messages"),
)


# Students
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)student/classes/$', 'student_classes', {}, name = "student_classes"),
    url(r'^(?i)student/classes/(?P<username>[\w.@+-]+)/$', 'student_classes', {}, name = "student_classes"),
    url(r'^(?i)student/messages/$', 'student_messages', {}, name = "student_messages"),
    url(r'^(?i)student/messages/(?P<username>[\w.@+-]+)/$', 'student_messages', {}, name = "student_messages"),
    url(r'^(?i)student/tutors/$', 'tutors', {}, name = "tutors"),
    url(r'^(?i)student/tutors/(?P<username>[\w.@+-]+)/$$', 'tutors', {}, name = "tutors"),
)

urlpatterns += patterns('apps.profile.views.ajax',
    url(r'^(?i)student/cancel_class/$', 'student_cancel_class', {}, name = "student_cancel_class"),
    url(r'^(?i)student/rate_tutor/$', 'student_rate_tutor', {}, name = "student_rate_tutor"),
    url(r'^(?i)student/add_interest/$', 'add_interest', {}, name = "add_interest"),
    url(r'^(?i)student/remove_interest/$', 'remove_interest', {}, name = "remove_interest"),
    url(r'^(?i)student/remove_interest/(?P<subject_id>\d+)/$', 'remove_interest', {}, name = "remove_interest"),
    url(r'^(?i)student/send-parent-request/$', 'send_parent_request', {}, name = "send_parent_request"),

    url(r'^(?i)ajax-class-week/$', 'ajax_week_classes', {}, name = "ajax_week_classes"),
    url(r'^(?i)ajax-class-week/(?P<date>[\d\-]+)/$', 'ajax_week_classes', {}, name = "ajax_week_classes"),
    url(r'^(?i)ajax-class-week/(?P<date>[\d\-]+)/(?P<is_tutor>\d)/$', 'ajax_week_classes', {}, name = "ajax_week_classes"),
)


# Common
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)parent/add_child/$', 'add_child', {}, name = "add_child"),
    url(r'^(?i)newsletter_verify_email_address/(?P<key>[\w\-\_]+)/$', 'newsletter_verify_email_address', {}, name = "newsletter_verify_email_address"),
)

urlpatterns += patterns('apps.profile.views.ajax',
    url(r'^(?i)add_newsletter_subscription/$', 'add_newsletter_subscription', name = "add_newsletter_subscription"),

    
    url(r'^(?i)view_modal_messages/(?P<username>[\w.@+-]+)/$', 'view_modal_messages', {}, name = "view_modal_messages"),
    #url(r'^(?i)view_modal_messages/(?P<username>[\w.@+-]+)/$', 'view_modal_messages', {}, name = "view_modal_messages"),
    url(r'^(?i)view_modal_messages/(?P<username>[\w.@+-]+)/(?P<to>\d+)/$', 'view_modal_messages', {}, name = "view_modal_messages"),
    url(r'^(?i)view_modal_messages/(?P<username>[\w.@+-]+)/(?P<to>\d+)/$', 'view_modal_messages', {}, name = "view_modal_messages"),
    url(r'^(?i)view_modal_messages/(?P<username>[\w.@+-]+)/(?P<to>\d+)/(?P<class_id>\d+)/$', 'view_modal_messages', {}, name = "view_modal_messages"),

    url(r'^(?i)send_modal_message/$', 'send_modal_message', {}, name = "send_modal_message"),
    url(r'^(?i)send_modal_message/(?P<to>\d+)/$', 'send_modal_message', {}, name = "send_modal_message"),
    url(r'^(?i)send_modal_message/(?P<to>\d+)/(?P<class_id>\d+)/$', 'send_modal_message', {}, name = "send_modal_message"),

    url(r'^(?i)referral-friend/$', 'referral_friend', {}, name = "referral_friend"),

    url(r'^(?i)get_user_image/$', 'get_user_data', {}, name = "get_user_data"),
    url(r'^(?i)get_user_image/(?P<user_id>\d+)/$', 'get_user_data', {}, name = "get_user_data"),
    
    url(r'^(?i)update_header/$', 'update_header', {}, name = "update_header"),
    
    url(r'^(?i)activate_discount/$', 'activate_discount', {}, name="activate_discount"),
    url(r'^(?i)preview_profile_image/$', 'preview_profile_image', {}, name="preview_profile_image"),
    url(r'^(?i)preview_profile_image_delete/$', 'preview_profile_image_delete', {}, name="preview_profile_image_delete"),

    url(r'^(?i)set_class_language/$', 'set_class_language', {}, name="set_class_language"),
    url(r'^(?i)set_class_language/(?P<language>[\w\_]+)/$', 'set_class_language', {}, name="set_class_language"),
)

urlpatterns += patterns('apps.profile.views.topup',
    url(r'^(?i)topup/cart/$', 'topup_cart', name = "topup_cart"),
    url(r'^(?i)topup/cart/(?P<username>[\w.@+-]+)/$', 'topup_cart', name = "topup_cart"),
    url(r'^(?i)topup/cancel/(?P<username>[\w.@+-]+)/$', 'topup_cancel', name = "topup_cancel"),
    url(r'^(?i)topup/cancel/(?P<username>[\w.@+-]+)/(?P<ajax>\d)/$', 'topup_cancel', name = "topup_cancel"),
    url(r'^(?i)topup/successful/(?P<username>[\w.@+-]+)/$', 'topup_successful', name = "topup_successful"),
    url(r'^(?i)withdraw/manual/$', 'withdraw', name = "withdraw"),
)





