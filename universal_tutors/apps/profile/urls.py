from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib import admin

# Registration/Login views
urlpatterns = patterns('apps.profile.views.login',
    url(r"^(?i)account/signup/$", 'signup',  name="signup"),
    url(r"^(?i)account/signin/$", 'signin', name="login"),
    url(r"^(?i)account/logout/$", 'logout_view', name="logout"),
    url(r"^(?i)account/successfull/-signup/$", 'successfull_signup', name="successfull_signup"),
)

# Front-end profile
urlpatterns += patterns('apps.profile.views.main',
    url(r"^(?i)dashboard/$", 'dashboard', name="dashboard"),
    url(r'^(?i)profile/$', 'profile', {}, name = "profile"),
    url(r'^(?i)profile/(?P<username>[\w\-\_]+)/$', 'profile', {}, name = "profile"),
    url(r'^(?i)tutor/profile/edit/$', 'edit_tutor_profile', {}, name = "edit_tutor_profile"),
    url(r'^(?i)student/profile/edit/$', 'edit_student_profile', {}, name = "edit_student_profile"),
    url(r'^(?i)parent/profile/edit/$', 'edit_parent_profile', {}, name = "edit_parent_profile"),

    url(r'^(?i)history/$', 'history', {}, name = "history"),
    url(r'^(?i)history/(?P<username>[\w\-\_]+)/$', 'history', {}, name = "history"),
)

# Tutors
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)tutor/classes/$', 'tutor_classes', {}, name = "tutor_classes"),
    url(r'^(?i)tutor/messages/$', 'tutor_messages', {}, name = "tutor_messages"),
    url(r'^(?i)tutors/$', 'tutors', {}, name = "tutors"),

    url(r'^(?i)book-class/(?P<username>[\w\-\_]+)/$', 'book_class', {}, name = "book_class"),
    url(r'^(?i)tutor/report/(?P<username>[\w\-\_]+)/$', 'report', {}, name = "report"),
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

    url(r'^(?i)tutor/cancel_class/$', 'tutor_cancel_class', {}, name = "tutor_cancel_class"),
    url(r'^(?i)tutor/rate_student/$', 'tutor_rate_student', {}, name = "tutor_rate_student"),
    
    url(r'^(?i)tutor/favorite/$', 'favorite', {}, name = "favorite"),
    url(r'^(?i)tutor/favorite/(?P<person_id>\d+)/$', 'favorite', {}, name = "favorite"),

    url(r'^(?i)confirm-book-class/$', 'book_class', {}, name = "confirm_book_class"),
 
    url(r'^(?i)ajax-book-class/(?P<username>[\w\-\_]+)/$', 'ajax_book_class', {}, name = "ajax_book_class"),
    url(r'^(?i)ajax-book-class/(?P<username>[\w\-\_]+)/(?P<date>[\d\-]+)/$', 'ajax_book_class', {}, name = "ajax_book_class"),
)

# Students
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)student/classes/$', 'student_classes', {}, name = "student_classes"),
    url(r'^(?i)student/messages/$', 'student_messages', {}, name = "student_messages"),
)

urlpatterns += patterns('apps.profile.views.ajax',
    url(r'^(?i)student/cancel_class/$', 'student_cancel_class', {}, name = "student_cancel_class"),
    url(r'^(?i)student/rate_tutor/$', 'student_rate_tutor', {}, name = "student_rate_tutor"),
    url(r'^(?i)student/add_interest/$', 'add_interest', {}, name = "add_interest"),
    url(r'^(?i)student/remove_interest/$', 'remove_interest', {}, name = "remove_interest"),
    url(r'^(?i)student/remove_interest/(?P<subject_id>\d+)/$', 'remove_interest', {}, name = "remove_interest"),
    url(r'^(?i)student/send-parent-request/$', 'send_parent_request', {}, name = "send_parent_request"),

    url(r'^(?i)student/add_credits/$', 'add_credits', {}, name = "add_credits"),
    url(r'^(?i)student/add_credits/(?P<username>[\w\-\_]+)/$', 'add_credits', {}, name = "add_credits"),

)


# Common
urlpatterns += patterns('apps.profile.views.main',
    url(r'^(?i)newsletter_verify_email_address/(?P<key>[\w\-\_]+)/$', 'newsletter_verify_email_address', {}, name = "newsletter_verify_email_address"),
)

urlpatterns += patterns('apps.profile.views.ajax',
    url(r'^(?i)add_newsletter_subscription/$', 'add_newsletter_subscription', name = "add_newsletter_subscription"),

    url(r'^(?i)view_modal_messages/$', 'view_modal_messages', {}, name = "view_modal_messages"),
    url(r'^(?i)view_modal_messages/(?P<to>\d+)/$', 'view_modal_messages', {}, name = "view_modal_messages"),
    url(r'^(?i)view_modal_messages/(?P<to>\d+)/(?P<class_id>\d+)/$', 'view_modal_messages', {}, name = "view_modal_messages"),

    url(r'^(?i)send_modal_message/$', 'send_modal_message', {}, name = "send_modal_message"),
    url(r'^(?i)send_modal_message/(?P<to>\d+)/$', 'send_modal_message', {}, name = "send_modal_message"),
    url(r'^(?i)send_modal_message/(?P<to>\d+)/(?P<class_id>\d+)/$', 'send_modal_message', {}, name = "send_modal_message"),

    url(r'^(?i)parent/add_child/$', 'add_child', {}, name = "add_child"),
)






