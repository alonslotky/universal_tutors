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

from apps.profile.forms import SigninForm, SignupForm, TutorSignupForm


def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect(reverse('home'))

def signin(request, *args, **kwargs):

    next = request.REQUEST.get('next', reverse('profile'))
    
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next)

    kwargs.update({
        'form_class': SigninForm,
        'success_url': next
    })

    return login(request, *args, **kwargs)


def signup(request, *args, **kwargs):
    # next = request.REQUEST.get('next', reverse('profile'))
    user_type = int(request.GET.get('user_type', 0))
    
    if user_type == 1:
        form = TutorSignupForm
        next = reverse('edit_tutor_profile')
    elif user_type == 2:
        form = SignupForm
        next = reverse('edit_student_profile')
    elif user_type == 3:
        form = SignupForm
        next = reverse('edit_parent_profile')
    else:
        form = SignupForm
        next = reverse('home')
    
    kwargs.update({
        'form_class': form,
        # 'success_url': request.REQUEST.get('next', reverse('profile')),
        'success_url': next,
    })
    
    return allauth_signup(request, *args, **kwargs)