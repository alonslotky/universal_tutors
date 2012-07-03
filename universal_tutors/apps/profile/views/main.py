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

    classes = chain(
        profile.waiting_classes(),
        profile.booked_classes(),
        profile.other_classes(),
    )
    
    return {
        'profile': profile,
        'person': user,
        'classes': classes
    }


@login_required
@over16_required()
@main_render(template='profile/tutor/messages.html')
def tutor_messages(request):
    """
    view my recent activity
    """
    user = request.user

    usermessages = User.objects.select_related().filter(sent_messages__to = user).annotate(max_date = Max('sent_messages__created')).order_by('-max_date')

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

    classes = chain(
        profile.booked_classes(),
        profile.waiting_classes(),
        profile.other_classes(),
    )
    
    return {
        'profile': profile,
        'person': user,
        'classes': classes
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

    usermessages = User.objects.select_related().filter(sent_messages__to = person).annotate(max_date = Max('sent_messages__created')).order_by('-max_date')

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
    favorite = User.objects.select_related().filter(profile__favorite=user).distinct()
    used = User.objects.select_related().filter(classes_as_tutor__student=user, classes_as_tutor__status__in = [Class.STATUS_TYPES.BOOKED, Class.STATUS_TYPES.DONE]).distinct()

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
            return http.HttpResponseRedirect('%s#children' % reverse('edit_parent_profile'))
    
    return {
        'form': form,
    }

