import urllib

from django.core.urlresolvers import reverse
from django import http
from django.db.models import Q
from django.template import Context, loader
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage

from allauth.account.views import signup as allauth_signup, login

from apps.profile.forms import SigninForm, SignupForm


def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect(reverse('home'))

def signin(request, *args, **kwargs):

    next = request.REQUEST.get('next', reverse('dashboard'))
    
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next)

    kwargs.update({
        'form_class': SigninForm,
        'success_url': next
    })

    return login(request, *args, **kwargs)


def signup(request, *args, **kwargs):
    next = request.REQUEST.get('next', reverse('dashboard'))

    kwargs.update({
        'form_class': SignupForm,
        'success_url': request.REQUEST.get(next, reverse('dashboard')),
    })
    
    return allauth_signup(request, *args, **kwargs)
