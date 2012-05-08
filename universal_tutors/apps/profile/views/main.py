from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings

from allauth.facebook.models import FacebookAccount
from allauth.twitter.models import TwitterAccount
from allauth.openid.models import OpenIDAccount
from allauth.socialaccount.forms import DisconnectForm

from apps.common.utils.view_utils import main_render
from apps.common.utils.decorators import over16_required
from apps.profile.models import UserProfile, NewsletterSubscription
from apps.profile.forms import *

import pytz

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

    if profile.type == profile.TYPES.TUTOR:
        template = 'profile/tutor/profile.html'
    elif profile.type == profile.TYPES.STUDENT or profile.type == profile.TYPES.UNDER16:
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
    }


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
            return http.HttpResponseRedirect(reverse('profile'))

    return {
        'profile':profile,
        'form': form,
        'subject_formset': subject_formset,
        'qualifications_formset': qualifications_formset,
        'timezones': pytz.common_timezones,
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

    return {
        'profile':profile,
    }


@login_required
@over16_required()
@main_render(template='profile/tutor/messages.html')
def tutor_messages(request):
    """
    view my recent activity
    """
    user = request.user

    usermessages = User.objects.select_related().filter(sent_messages__to = user).distinct()

    return {
        'usermessages':usermessages,
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
    }
    
    form = ProfileForm(request.POST or None, request.FILES or None, initial=data, instance = profile)
    if request.POST:
        if form.is_valid():
            form.save()
            profile.update_tutor_information(form)
            request.session['django_timezone'] = pytz.timezone(profile.timezone)

            return http.HttpResponseRedirect(reverse('profile'))

    return {
        'profile':profile,
        'form': form,
        'timezones': pytz.common_timezones,
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

    return {
        'person': person,
        'profile':profile,
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

    usermessages = User.objects.select_related().filter(sent_messages__to = person).distinct()

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

    favorite_and_used = User.objects.select_related().filter(profile__favorite=user, classes_as_tutor__student=user, classes_as_tutor__status = Class.STATUS_TYPES.DONE).distinct()
    favorite = User.objects.select_related().exclude(profile__favorite=user, classes_as_tutor__student=user, classes_as_tutor__status = Class.STATUS_TYPES.DONE).filter(profile__favorite=user).distinct()
    used = User.objects.select_related().exclude(profile__favorite=user, classes_as_tutor__student=user, classes_as_tutor__status = Class.STATUS_TYPES.DONE).filter(classes_as_tutor__student=user, classes_as_tutor__status = Class.STATUS_TYPES.DONE).distinct()

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
        'tutor_groups': tutor_groups
    }


@login_required
@over16_required()
@main_render(template='profile/tutor/report.html')
def report(request, username):
    """
    view my recent activity
    """
    user = request.user
    
    tutor = get_object_or_404(User, username = username)
    
    success = False
    if request.method == 'POST':
        description = request.POST.get('violation-description')
        user.sent_report.create(violator=tutor, description=description)
        success = True

    return {
        'tutor': tutor,
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
    tutor = get_object_or_404(User, username = username)
    
    return {
        'person': tutor,
        'profile': tutor.profile,
        'date': datetime.date.today(),
    }
    
    
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
            return http.HttpResponseRedirect(reverse('profile'))

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

