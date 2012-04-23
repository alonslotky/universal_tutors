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
from apps.profile.forms import ProfileForm, EditProfileForm


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

    if profile.type == profile.TYPES.TUTOR:
        template = 'profile/tutor/profile.html'
    elif profile.type == profile.TYPES.STUDENT:
        template = ''
    else:
        raise http.Http404()

    return {
        'dashboard': person == user,
        'profile': profile,
        'TEMPLATE': template,
    }


@login_required
@main_render(template='profile/edit_profile.html')
def edit_profile(request):
    """
    edit my personal profile
    """
    user = request.user
    profile = user.profile

    social_form = None
    form = None

    if request.POST:
        if request.POST.get('social-form', ''):
            social_form = DisconnectForm(request.POST, user=request.user)
            if social_form.is_valid():
                messages.add_message(request, messages.INFO,
                                     'The social account has been disconnected')
                social_form.save()
                social_form = None

        else:
            form = EditProfileForm(request.POST)
            if form.is_valid():
                success = profile.update_information(form)
                if success:
                    return http.HttpResponseRedirect(reverse('my_profile'))

    if not form:
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'title': profile.title if profile.title else '',
            'about': profile.about if profile.about else '',
            'email': user.email if user.email else '',
            'country': profile.country,
            'location': profile.location if profile.location else '',
            'address': profile.address if profile.address else '',
            'postcode': profile.postcode if profile.postcode else '',
        }

        form = EditProfileForm(initial=data)

    if not social_form:
        social_form = DisconnectForm(user=request.user)

    return {
        'dashboard': True,
        'profile':profile,
        'form': form,
        'social_form': social_form,
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
    profile = user.profile

    return {
        'profile':profile,
    }


### STUDENTS #####################################################
@login_required
@over16_required()
@main_render(template='profile/student/classes.html')
def student_classes(request):
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
@main_render(template='profile/student/messages.html')
def student_messages(request):
    """
    view my recent activity
    """
    user = request.user
    profile = user.profile

    return {
        'profile':profile,
    }