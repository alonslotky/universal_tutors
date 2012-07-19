from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.db.models import Max
from itertools import chain

from allauth.facebook.models import FacebookAccount
from allauth.twitter.models import TwitterAccount
from allauth.openid.models import OpenIDAccount
from allauth.socialaccount.forms import DisconnectForm

from apps.common.utils.view_utils import main_render
from apps.common.utils.decorators import over16_required
from apps.profile.models import UserProfile, NewsletterSubscription
from apps.profile.forms import *
from apps.classes.models import *
from apps.classes.settings import MINIMUM_CREDITS_PER_HOUR

import pytz, datetime

@main_render()
def profile(request, username=None):
    """
    detailed profile from a user
    """
    user = request.user

    if username:
        person = get_object_or_404(User, username = username)
    elif user.is_authenticated():
        person = user
    else:
        raise http.Http404()

    profile = person.profile
    parent = profile.parent if profile.type == profile.TYPES.UNDER16 else None
    reviews = None
    can_send_message = True
    if profile.type == profile.TYPES.TUTOR:
        reviews = person.reviews_as_tutor.filter(is_active=True)
        template = 'profile/tutor/profile.html'
    elif profile.type == profile.TYPES.STUDENT or profile.type == profile.TYPES.UNDER16:
        if not Message.objects.filter(Q(user=person, to=user) | Q(user=user, to=person)) and \
            not user.classes_as_tutor.filter(student=person) and not profile.parent == user:
            can_send_message = False
        template = 'profile/student/profile.html'
    elif profile.type == profile.TYPES.PARENT:
        template = 'profile/parent/profile.html'
    else:
        raise http.Http404()

    return {
        'owner': person == user,
        'person': person,
        'profile': profile,
        'TEMPLATE': template,
        'parent': parent,
        'reviews': reviews,
        'user': user,
        'can_send_message': can_send_message
    }


@login_required
def edit_profile(request):
    """
    detailed profile from a user
    """
    user = request.user
    profile = user.profile

    if profile.type == profile.TYPES.TUTOR:
        return http.HttpResponseRedirect(reverse('edit_tutor_profile'))
    elif profile.type == profile.TYPES.STUDENT or profile.type == profile.TYPES.UNDER16:
        return http.HttpResponseRedirect(reverse('edit_student_profile'))
    elif profile.type == profile.TYPES.PARENT:
        return http.HttpResponseRedirect(reverse('edit_parent_profile'))
    else:
        raise http.Http404()


@login_required
@main_render(template='profile/tutor/edit_profile/base.html')
def edit_tutor_profile(request):
    """
    edit my personal profile
    """
    user = request.user
    profile = user.profile

    if profile.type != profile.TYPES.TUTOR:
        raise http.Http404()

    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'account_email': user.email,
    }


    form = ProfileForm(request.POST or None, request.FILES or None, initial=data, instance = profile)
    subject_formset = TutorSubjectFormSet(request.POST or None, request.FILES or None, instance=user)
    qualifications_formset = TutorQualificationFormSet(request.POST or None, request.FILES or None, instance=user)
    if request.POST:
        success = True
        
        if form.is_valid():
            form.save()
            profile.update_tutor_information(form)
            request.session['django_timezone'] = pytz.timezone(profile.timezone)
        else:
            success = False

        if subject_formset.is_valid():
            subject_formset.save()
        else:
            success = False

        if qualifications_formset.is_valid():
            qualifications_formset.save()
        else:
            success = False

        if success:
            return http.HttpResponseRedirect(reverse('edit_profile'))

    return {
        'MINIMUM_CREDITS_PER_HOUR': MINIMUM_CREDITS_PER_HOUR,
        'profile':profile,
        'form': form,
        'subject_formset': subject_formset,
        'qualifications_formset': qualifications_formset,
        'timezones': pytz.common_timezones,
        'date': datetime.date.today(),
        'class_subjects': ClassSubject.objects.all(),
    }


@login_required
@main_render(template='profile/dashboard.html')
def under16(request):
    """
    view my recent activity
    """
    user = request.user
    profile = user.profile

    return {
        'dashboard': True,
        'profile':profile,
    }

@login_required
@over16_required()
@main_render(template='profile/dashboard.html')
def dashboard(request):
    """
    view my recent activity
    """
    user = request.user
    profile = user.profile

    return http.HttpResponseRedirect('home')

#    return {
#        'dashboard': True,
#        'profile':profile,
#    }

@main_render(template='profile/newsletter_email_verify.html')
def newsletter_verify_email_address(request, key):
    subscription = get_object_or_404(NewsletterSubscription, hash_key=key)

    existing = False
    if subscription.email_verified:
        existing = True

    subscription.verify_email()

    return {'existing': existing}



### TUTORS #####################################################
@login_required
@over16_required()
@main_render(template='profile/tutor/classes.html')
def tutor_classes(request):
    """
    view my recent activity
    """
    user = request.user
    profile = user.profile

    classes_groups = [{
       'title': 'Upcoming Classes',
       'classes': profile.upcoming_classes(),
       'empty': "You have no upcoming classes",
    }, {
       'title': 'Cancelled Classes',
       'classes': profile.cancelled_classes(),
       'empty': "You have no cancelled classes",
    }, {
       'title': 'Taken Classes',
       'classes': profile.taken_classes(),
       'empty': "You have not given any classes",
    }]
    
    return {
        'profile': profile,
        'person': user,
        'classes_groups': classes_groups,
    }


@login_required
@over16_required()
@main_render(template='profile/tutor/messages.html')
def tutor_messages(request):
    """
    view my recent activity
    """
    user = request.user
    old = datetime.datetime(2000,1,1) # just a hold date

    usermessages = User.objects.select_related() \
                    .filter(Q(sent_messages__to = user) | Q(received_messages__user = user)) \
                    .annotate(max_sent = Max('sent_messages__created'), max_received = Max('received_messages__created'))
    usermessages = sorted(usermessages, cmp=lambda y,x: cmp(max(x.max_sent, x.max_received) or old, max(y.max_sent, y.max_received) or old))


    return {
        'usermessages':usermessages,
    }

@login_required
@main_render('profile/tutor/test_class.html')
def test_class(request):
    """
    detailed profile from a user
    """
    user = request.user
    profile = user.profile

    if profile.type != profile.TYPES.TUTOR:
        raise http.Http404()
    
    if not profile.test_class_minutes:
        return http.HttpResponseRedirect(reverse('edit_tutor_profile'))
    
    return {
        'profile': profile,
    }


### STUDENTS #####################################################
@login_required
@main_render(template='profile/student/edit_profile/base.html')
def edit_student_profile(request):
    """
    edit my personal profile
    """
    user = request.user
    profile = user.profile

    if profile.type != profile.TYPES.STUDENT and profile.type != profile.TYPES.UNDER16:
        raise http.Http404()

    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'account_email': user.email,
    }
    
    form = ProfileForm(request.POST or None, request.FILES or None, initial=data, instance = profile)
    interest_formset = StudentInterestFormSet(request.POST or None, request.FILES or None, instance=user)
    if request.POST:
        success = True
        if form.is_valid():
            form.save()
            profile.update_tutor_information(form)
            request.session['django_timezone'] = pytz.timezone(profile.timezone)
        else:
            success = False
            
        if interest_formset.is_valid():
            interest_formset.save()
        else:
            success = False
        
        if success:
            return http.HttpResponseRedirect(reverse('edit_profile'))

    return {
        'profile':profile,
        'form': form,
        'timezones': pytz.common_timezones,
        'interest_formset': interest_formset,
        'date': datetime.date.today(),
        'class_subjects': ClassSubject.objects.all(),
    }


@login_required
@over16_required()
@main_render(template='profile/student/classes.html')
def student_classes(request, username=None):
    """
    view my recent activity
    """

    user = request.user

    if username:
        person = get_object_or_404(User, username = username)
        if person != user and person.profile.parent != user:
            raise http.Http404()
    elif user.is_authenticated():
        person = user
    else:
        raise http.Http404()

    profile = person.profile
    type = None
    if request.POST:
        type = request.POST.get('type', None)
        if type == 'all':
            classes_groups = [{
               'title': 'Upcoming Classes',
               'classes': profile.upcoming_classes(),
               'empty': "You have no upcoming classes",
            }, {
               'title': 'Completed Classes',
               'classes': profile.taken_classes(),
               'empty': "You have not taken any classes",
            }, {
               'title': 'Cancelled Classes',
               'classes': profile.cancelled_classes(),
               'empty': "You have no cancelled classes",
            }]
        elif type == 'upcoming':
            classes_groups = [{
               'title': 'Upcoming Classes',
               'classes': profile.upcoming_classes(),
               'empty': "You have no upcoming classes",
            }]
        elif type == 'completed':
            classes_groups = [{
               'title': 'Completed Classes',
               'classes': profile.taken_classes(),
               'empty': "You have not taken any classes",
            }]
        elif type == 'cancelled':
            classes_groups = [{
               'title': 'Cancelled Classes',
               'classes': profile.cancelled_classes(),
               'empty': "You have no cancelled classes",
            }]
            
    else:
        classes_groups = [{
           'title': 'Upcoming Classes',
           'classes': profile.upcoming_classes(),
           'empty': "You have no upcoming classes",
        }, {
           'title': 'Completed Classes',
           'classes': profile.taken_classes(),
           'empty': "You have not taken any classes",
        }, {
           'title': 'Cancelled Classes',
           'classes': profile.cancelled_classes(),
           'empty': "You have no cancelled classes",
        }]
    
    
    return {
        'profile': profile,
        'person': user,
        'classes_groups': classes_groups,
        'type': type,
    }


@login_required
@over16_required()
@main_render(template='profile/student/messages.html')
def student_messages(request, username=None):
    """
    view my recent activity
    """

    user = request.user

    if username:
        person = get_object_or_404(User, username = username)
    elif user.is_authenticated():
        person = user
    else:
        raise http.Http404()

    profile = user.profile

    old = datetime.datetime(2000,1,1) # just a hold date

    usermessages = User.objects.select_related() \
                    .filter(Q(sent_messages__to = person) | Q(received_messages__user = person)) \
                    .annotate(max_sent = Max('sent_messages__created'), max_received = Max('received_messages__created'))
    usermessages = sorted(usermessages, cmp=lambda y,x: cmp(max(x.max_sent, x.max_received) or old, max(y.max_sent, y.max_received) or old))

    return {
        'usermessages':usermessages,
        'person': person,
        'profile': profile,
    }
    
@login_required
@over16_required()
@main_render('profile/tutor/tutors.html')
def tutors(request):
    """
    tutors list
    """
    user = request.user
    
    tutor_groups = []

    favorite_and_used = User.objects.select_related().filter(profile__favorite=user, classes_as_tutor__student=user).distinct()
    favorite = User.objects.select_related().filter(profile__favorite=user).exclude(classes_as_tutor__student=user).distinct()
    used = User.objects.select_related().filter(classes_as_tutor__student=user).exclude(profile__favorite=user).distinct()

    if favorite_and_used:
        tutor_groups.append({
        'title': 'Favorite & Used Tutors',
        'tutors': favorite_and_used,        
        })

    if favorite:
        tutor_groups.append({
        'title': 'Favorite Tutors',
        'tutors': favorite,        
        })

    if used:
        tutor_groups.append({
        'title': 'Used Tutors',
        'tutors': used,        
        })

    return {
        'tutor_groups': tutor_groups,
        'user': user
    }


@login_required
@over16_required()
@main_render(template='profile/report.html')
def report(request, username):
    """
    view my recent activity
    """
    user = request.user
    
    person = get_object_or_404(User, username = username)
    
    success = False
    if request.method == 'POST':
        description = request.POST.get('violation-description')
        user.sent_report.create(violator=person, description=description)
        success = True

    return {
        'person': person,
        'person_profile': person.profile,
        'success': success,
    }


@login_required
@over16_required()
@main_render(template='profile/tutor/book_class/base.html')
def book_class(request, username):
    """
    view my recent activity
    """
    user = request.user
    tutor = get_object_or_404(User, username = username, profile__type = UserProfile.TYPES.TUTOR)
    
    return {
        'person': tutor,
        'profile': tutor.profile,
        'date': datetime.date.today(),
        'week': tutor.profile.get_week(gtz = user.profile.timezone),
    }


@main_render(template='profile/tutor/crb_form.html')
def crb_form(request):
    """
    redirect for CRB form
    """
    return {}

    
    
### PARENT #####################################################

@login_required
@main_render(template='profile/parent/edit_profile/base.html')
def edit_parent_profile(request):
    """
    edit my personal profile
    """
    user = request.user
    profile = user.profile

    if profile.type != profile.TYPES.PARENT:
        raise http.Http404()

    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'account_email': user.email,
    }
    
    form = ProfileForm(request.POST or None, request.FILES or None, initial=data, instance = profile)
    if request.POST:
        success = True
        
        if form.is_valid():
            form.save()
            profile.update_tutor_information(form)
            request.session['django_timezone'] = pytz.timezone(profile.timezone)
        else:
            success = False

        if success:
            return http.HttpResponseRedirect(reverse('edit_profile'))

    return {
        'profile':profile,
        'form': form,
        #'subject_formset': subject_formset,
        #'qualifications_formset': qualifications_formset,
        'timezones': pytz.common_timezones,
    }


@login_required
@main_render(template='profile/history.html')
def history(request, username=None):
    """
    detailed profile from a user
    """

    if username:
        user = request.user
        person = get_object_or_404(User, username=username)
        profile = person.profile
        if user != person and profile.parent != user:
            raise http.Http404()
    else:
        person = request.user

    return { 'person': person }


@login_required
@main_render('account/children-signup.html')
def add_child(request):
    user = request.user
    profile = user.profile
    
    if profile.type != profile.TYPES.PARENT:
        raise http.Http404()

    form = Under16SignupForm(request.POST or None, parent=user)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(request=request)
            profile = user.profile
            for p in request.FILES.getlist('profile_image'):
                profile.profile_image.save(p.name, p)
                profile.save()
            return http.HttpResponseRedirect('%s#children' % reverse('edit_parent_profile'))
    
    return {
        'form': form,
        'class_subjects': ClassSubject.objects.all(),
    }

