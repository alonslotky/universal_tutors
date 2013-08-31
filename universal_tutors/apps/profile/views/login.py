import urllib
import pytz
import datetime
from django.db import models
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
from django.contrib.formtools.wizard.views import SessionWizardView,NamedUrlWizardView
#from django.contrib.formtools.wizard import FormWizard
from django.contrib.auth.models import User

from allauth.socialaccount import helpers
from allauth.account.views import login
from allauth.account.utils import get_default_redirect, user_display, complete_signup 
# from allauth.account.views import signup as allauth_signup, login
from allauth.socialaccount.views import connections
from allauth.utils import passthrough_login_redirect_url

from apps.common.utils.view_utils import handle_uploaded_file
from apps.classes.models import ClassSubject
from apps.profile.forms import *
from apps.core.models import Currency
from apps.profile.models import WeekAvailability
from django.http import HttpResponse

import json

#from avatar import *

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


def student_signup_old(request, *args, **kwargs):
    form = StudentSignupForm_new
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
         #("step6", forms.MultiPartSignupFormStep6),
         ]

part11 = [("step1", forms.MultiPartSignupFormStep1),]
part12 = [("step2", forms.MultiPartSignupFormStep2),
         ("step3", forms.MultiPartSignupFormStep3),
         ("step4", forms.MultiPartSignupFormStep4),
         ("step5", forms.MultiPartSignupFormStep5),
         #("step6", forms.MultiPartSignupFormStep6),
         ]         

#account/home_tutor_singup.html
#../apps/core/templates/core/home_new_intg.html

TUTOR_SIGNUP_TEMPLATES = {"step1": "account/home_tutor_signup.html",
             "step2": "account/tutor_signup_step2.html",
             "step3": "account/tutor_signup_step3.html",
             "step4": "account/tutor_signup_step4.html",
             "step5": "account/tutor_signup_step5.html",
             "step6": "account/tutor_signup_step6.html",}

#def photo1(request):
#    if request.method == 'POST': # If the form has been submitted...
#        form = avatar.forms.UploadAvatarForm(request.POST) # A form bound to the POST data
#        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
#            return HttpResponseRedirect('/thanks/') # Redirect after POST
#    else:
#        form = ContactForm() # An unbound form

#    return render(request, 'photo.html', {
#        'form': form,
#    })

#def photo(request):
#    return render_to_response('account/photo.html')

class TutorSignupWizard(SessionWizardView):
#class TutorSignupWizard(NamedUrlWizardView):
    
    def get_form_prefix(self, step=None, form=None):
        return ''
    
        
    def get_template_names(self):
        return [TUTOR_SIGNUP_TEMPLATES[self.steps.current]]        
    
    def save_genres(self, form_list, user):
        #get genres from from data and add it to the user!
        user.profile.genres = Genre.objects.filter(id__in = [int(id) for id in form_list[2].data.getlist('genres')])
        
    def save_tutor(self, form_list, **kwargs):
      
        form_data = [form.cleaned_data for form in form_list]
        '''
        [{'password1': u'1234', 'first_name': u'alon', 'last_name': u'slotky', 'email': u'alonslotky@yahoo.com', 'password2': u'1234'}, 
         {'first_name': u'alon', 'last_name': u'slotky', 'gender': u'0', 'in_person_tutoring': True, 'zipcode': 1231, 'date_of_birth': datetime.date(1974, 1, 1), 'email': u'alonslotky@yahoo.com', 'online_tutoring': True}, 
         {},
        {'currency': u'3', 'price_per_hour': Decimal('150')}, 
         None]
        '''
        {"82618670":{"weekday":"2","begin_hour":6,"begin_minute":15,"end_hour":10,"end_minute":30}}
        availability_periods = json.loads(form_list[4].data['availability'])
        image = None
        session_key = ''

        session_key = self.request.session.session_key
        try:
            image = UploadProfileImage.objects.get(key=session_key).image
        except UploadProfileImage.DoesNotExist:
            pass

        user = User()

        password = form_data[0]['password1']
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.is_active = True
        user.username = (form_data[0]['email']) #temp maybe add user field??
        user.first_name = form_data[0]['first_name']
        user.last_name = form_data[0]['last_name']
        user.email = form_data[0]['email']
        user.save()
        
        profile = user.profile        
        #profile.country = self.cleaned_data['country']
        #profile.referral = int(self.cleaned_data.get('referral', 0))
        #profile.other_referral = self.cleaned_data.get('referral_other', None)
        #profile.referral_key = self.cleaned_data.get('referral_key', None)
        profile.gender = form_data[1].get('gender', 0)
        profile.timezone = form_data[1].get('timezone', None)
        profile.currency = Currency.objects.get(id=form_data[3].get('currency', 1))
        profile.price_per_hour = form_data[3].get('price_per_hour', -1)
        profile.date_of_birth = form_data[1].get('date_of_birth')
        profile.zipcode = form_data[1].get('zipcode', 0) 
        profile.about = form_data[3].get('about', 0)   
        profile.country = form_data[1].get('country', None)
        profile.agreement = form_data[4].get('agreement', None)
        profile.newsletter = form_data[4].get('newsletter', None)
        profile.partners_newsletter = form_data[4].get('partners_newsletter', None)
        #profile.timezone = form_data[1].get('timezone', 0)
        profile.referred_by_friend = form_data[3].get('referred_by_friend', 0) 

        user.profile.genres = Genre.objects.filter(id__in = [int(id) for id in form_list[2].data.getlist('genres')])
        #self.save_genres(form_list, user)
        
        #availability
        for key, val in availability_periods.items():
            #val_example = {"begin_hour":6,"begin_minute":15,"end_hour":10,"end_minute":30}
            availability = WeekAvailability()
            availability.weekday = int(val['weekday'])
            new_object = True
            
            availability.begin = datetime.time(hour = val['begin_hour'], minute = val['begin_minute'])
            availability.end = datetime.time(hour = val['end_hour'], minute = val['end_minute'])
            user.week_availability.add(availability)
        
        if image:
            profile.profile_image = image
        
        for p in self.request.FILES.getlist('profile_image'):
            profile.profile_image.save(p.name, p)
            profile.save()
    
        #profile.crb = self.cleaned_data.get('crb', False)
        
        if session_key:
            UploadProfileImage.objects.filter(key=session_key).update(image=None)
            UploadProfileImage.objects.filter(key=session_key).delete()        
        
        #TODO send_email_confirmation
        send_email_confirmation(user, request=self.request)
        
        #profile.about = self.cleaned_data.get('about', '')
        #profile.crb = self.cleaned_data.get('crb', False)
        #profile.webcam = self.cleaned_data.get('webcam', False)
        profile.type = profile.TYPES.TUTOR
        #profile.paypal_email = self.cleaned_data.get('paypal_email', None)
        #tutoring_type = self.cleaned_data.get('tutoring_type', 0)
        #TODO save tutoring type
        #TODO add currency
        profile.save()
         
        try:
            email = EmailTemplate.objects.get(type=profile.NOTIFICATIONS_TYPES.NEW_TUTOR)
            email.send_email({
                'user': user,
                'tutor': user,
                'profile': profile,
                'PROJECT_SITE_DOMAIN': settings.PROJECT_SITE_DOMAIN,
             }, [settings.SUPPORT_EMAIL])
        except EmailTemplate.DoesNotExist:
            pass
          
        return user
    
    def done(self, form_list, **kwargs):
        user = self.save_tutor(form_list)
        success_url = reverse('edit_tutor_profile')
        return complete_signup(self.request, user, success_url)
    
#    def get_form_kwargs(self, step):
#        if "step2" == step:
#            return {"request": self.request}
#        else:
#           return {}
    def get_form(self, step=None, data=None, files=None):
        form = super(TutorSignupWizard, self).get_form(step, data, files)
        
        if step is not None and data is not None:
            # get_form is called for validation by get_cleaned_data_for_step()
            return form

        elif step == "step1":
            
            data = self.get_cleaned_data_for_step('step1')
            if data is not None:
                form.fields['first_name'].initial = data.get('first_name')
                form.fields['last_name'].initial = data.get('last_name')
                form.fields['email'].initial = data.get('email')

        return form


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
    #fields = list(form)    
    #part1, part2 = fields[:4], fields[4:]
    #part1 = form[:4]
    next_url = reverse('edit_tutor_profile')

    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next_url)
    
    kwargs.update({
        'form_class': form,
        'success_url': next_url,
        'template_name': 'account/tutor-subjects.html',
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

def student_signup(request, *args, **kwargs):
    form = StudentSignupForm_simple
    next_url = reverse('edit_student_profile')
    
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(next_url)
    
    kwargs.update({
        'form_class': form,
        'success_url': next_url,
        'template_name': 'account/student-signup_new.html',
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

