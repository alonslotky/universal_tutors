import urllib
import pytz

from django.core.urlresolvers import reverse
from django import http
from django.db.models import Q
from django.template import Context, loader
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.contrib.formtools.wizard.views import SessionWizardView

from allauth.socialaccount import helpers
from allauth.account.views import login
from allauth.account.utils import get_default_redirect, user_display, complete_signup 
# from allauth.account.views import signup as allauth_signup, login
from allauth.socialaccount.views import connections
from allauth.utils import passthrough_login_redirect_url

from apps.common.utils.view_utils import handle_uploaded_file
from apps.classes.models import ClassSubject
from apps.profile.forms import *


def show_genres(request):
    return render_to_response("account/genres.html",
                          {'nodes':Genre.objects.all()},
                          context_instance=RequestContext(request))
    
def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect(reverse('home'))


def signin(request, *args, **kwargs):

    next = request.REQUEST.get('next', reverse('edit_profile'))
    
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next)

    kwargs.update({
        'form_class': SigninForm,
        'success_url': next
    })

    return login(request, *args, **kwargs)


def successfull_signup(request):
    l = [reverse('edit_tutor_profile'), reverse('edit_student_profile'), reverse('edit_parent_profile')]
    text = """
        <script>
            window.location='%s';
        </script>
    """ % l[int(request.GET.get('user_type')) - 1]
    
    return http.HttpResponse(text)


def student_signup(request, *args, **kwargs):
    form = StudentSignupForm
    next_url = reverse('edit_student_profile')
    
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next_url)

    kwargs.update({
        'form_class': form,
        'success_url': next_url,
        'template_name': 'account/student-signup.html',
        'extra_ctx': {
            'class_subjects': ClassSubject.objects.all(),
        }
    })
    
    return allauth_signup(request, *args, **kwargs)

from apps.profile import forms
TUTOR_SIGNUP_FORMS = [("step1", forms.MultiPartSignupFormStep1),
         ("step2", forms.MultiPartSignupFormStep2),
         ("step3", forms.MultiPartSignupFormStep3),
         ("step4", forms.MultiPartSignupFormStep4),
         ("step5", forms.MultiPartSignupFormStep5),
         ("step6", forms.MultiPartSignupFormStep6)]

TUTOR_SIGNUP_TEMPLATES = {"step1": "account/tutor_signup_step1.html",
             "step2": "account/tutor_signup_step2.html",
             "step3": "account/tutor_signup_step3.html",
             "step4": "account/tutor_signup_step4.html",
             "step5": "account/tutor_signup_step5.html",
             "step6": "account/tutor_signup_step6.html",}

class TutorSignupWizard(SessionWizardView):
        
    def get_template_names(self):
        return [TUTOR_SIGNUP_TEMPLATES[self.steps.current]]        
    
    def done(self, form_list, **kwargs):
        #TODO see what to do with the data
        return HttpResponseRedirect(reverse('edit_tutor_profile'))

def tutor_signup(request, *args, **kwargs):
    form = TutorSignupForm
    next_url = reverse('edit_tutor_profile')

    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next_url)
    
    kwargs.update({
        'form_class': form,
        'success_url': next_url,
        'template_name': 'account/tutor-signup.html',
    })
    
    return allauth_signup(request, *args, **kwargs)

def tutor_signup1(request, *args, **kwargs):
    form = TutorSignupForm
    next_url = reverse('edit_tutor_profile')

    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next_url)
    
    kwargs.update({
        'form_class': form,
        'success_url': next_url,
        'template_name': 'account/tutor3.html',
    })
    
    return allauth_signup(request, *args, **kwargs)

def parent_signup(request, *args, **kwargs):
    form = ParentSignupForm
    next_url = reverse('edit_parent_profile')
    
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next_url)
    
    kwargs.update({
        'form_class': form,
        'success_url': next_url,
        'template_name': 'account/parent-signup.html',
    })
    
    return allauth_signup(request, *args, **kwargs)

def allauth_signup(request, **kwargs):
    
    form_class = kwargs.pop("form_class", SignupForm)
    template_name = kwargs.pop("template_name", "account/signup.html")
    redirect_field_name = kwargs.pop("redirect_field_name", "next")
    success_url = kwargs.pop("success_url", None)
    extra_ctx = kwargs.pop("extra_ctx", {})
    
    if success_url is None:
        success_url = get_default_redirect(request, redirect_field_name)
    
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save(request=request)
            profile = user.profile
            for p in request.FILES.getlist('profile_image'):
                profile.profile_image.save(p.name, p)
                profile.save()
            return complete_signup(request, user, success_url)
    else:
        form = form_class()
    ctx = {"form": form,
           "login_url": passthrough_login_redirect_url(request,
                                                       reverse("account_login")),
           "redirect_field_name": redirect_field_name,
           "redirect_field_value": request.REQUEST.get(redirect_field_name) }
    ctx.update(extra_ctx)
    return render_to_response(template_name, RequestContext(request, ctx))


def signup(request, *args, **kwargs):
    # next = request.REQUEST.get('next', reverse('profile'))
    user_type = int(request.GET.get('user_type', 0))
    template_name = 'account/signup.html'
    
    if user_type == 1:
        form = TutorSignupForm
    elif user_type == 2:
        form = StudentSignupForm
        template_name = 'account/student-signup.html'
    elif user_type == 3:
        form = ParentSignupForm
    else:
        form = SignupForm
        
    next = reverse('successfull_signup')

    kwargs.update({
        'form_class': form,
        # 'success_url': request.REQUEST.get('next', reverse('profile')),
        'success_url': next + '?user_type=%s' % user_type,
    })
    
    return allauth_signup(request, *args, **kwargs)


def socialaccount_signup(request, *args, **kwargs):
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(reverse(connections))
    signup = request.session.get('socialaccount_signup')
    if not signup:
        return http.HttpResponseRedirect(reverse('account_login'))
    form_class = kwargs.pop("form_class", SignupForm)
    template_name = kwargs.pop("template_name", 
                               'socialaccount/signup.html')
    data = signup['data']
    extra_ctx = kwargs.pop("extra_ctx", {})
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save(request=request)
            user.last_name = data.get('last_name', '')
            user.first_name = data.get('first_name', '')
            user.save()
            account = signup['account']
            account.user = user
            account.sync(data)
            profile = user.profile
            for p in request.FILES.getlist('profile_image'):
                profile.profile_image.save(p.name, p)
                profile.save()
            return helpers.complete_social_signup(request, user, account)
    else:
        form = form_class(initial=data)
    dictionary = dict(site=Site.objects.get_current(),
                      account=signup['account'],
                      form=form)
    return render_to_response(template_name, 
                              dictionary, 
                              RequestContext(request, extra_ctx))


def social_signup(request, *args, **kwargs):
    # next = request.REQUEST.get('next', reverse('profile'))
    user_type = int(request.GET.get('user_type', 0))
    
    if user_type == 1:
        form = TutorSocialSignupForm
        template_name = 'account/tutor-signup.html'
    elif user_type == 2:
        form = StudentSocialSignupForm
        template_name = 'account/student-signup.html'
    elif user_type == 3:
        form = ParentSocialSignupForm
        template_name = 'account/parent-signup.html'
    else:
        template_name = 'socialaccount/signup.html'
        form = SocialSignupForm
        
    next = reverse('successfull_signup')
    
    kwargs.update({
        'form_class': form,
        # 'success_url': request.REQUEST.get('next', reverse('profile')),
        'success_url': next + '?user_type=%s' % user_type,
        'template_name': template_name,
    })
    if user_type == 2:
        kwargs.update({
            'extra_ctx': {
                  'class_subjects': ClassSubject.objects.all(),
            }
        })
    
    return socialaccount_signup(request, *args, **kwargs)

