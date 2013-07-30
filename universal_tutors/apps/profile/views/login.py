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
from django.shortcuts import render_to_response, redirect
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render_to_response
from django.contrib.formtools.wizard.views import SessionWizardView,NamedUrlWizardView
#from django.contrib.formtools.wizard import FormWizard
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from allauth.socialaccount import helpers
from allauth.account.views import login
from allauth.account.utils import get_login_redirect_url, user_display, complete_signup, send_email_confirmation, perform_login
# from allauth.account.views import signup as allauth_signup, login
from allauth.socialaccount.views import connections


from apps.common.utils.view_utils import handle_uploaded_file
from apps.classes.models import ClassSubject
from apps.profile.forms import *
from apps.core.models import Currency
from apps.profile.models import WeekAvailability

import json
import requests
import random

from allauth.socialaccount.models import SocialApp
try:
    facebook_app_id = SocialApp.objects.get(provider = 'facebook').client_id
except:
    print 'No facebook app in DB!'
    facebook_app_id = '293107754037794'
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

TUTOR_SIGNUP_STEP_INDICES = {
                             }

class TutorSignupWizard(SessionWizardView):
#class TutorSignupWizard(FormWizard):
    
    def get_form_prefix(self, step=None, form=None):
        return ''
    
        
    def get_template_names(self):
        return [TUTOR_SIGNUP_TEMPLATES[self.steps.current]]        
    
    def save_genres(self, genres_form, user):
        #get genres from from data and add it to the user!
        user.profile.save()
        user.profile.genres = Genre.objects.filter(id__in = [int(id) for id in genres_form.data.getlist('genres')])
        
    def save_tutor(self, form_list, is_social_signup, **kwargs):
        
        form_data = [form.cleaned_data for form in form_list]
        i = 0 if is_social_signup else 1
        form_data_indices = {"step1": 0, "step2": i, "step3": i+1, "step4": i+2, "step5": i+3}
        '''
        [{'password1': u'1234', 'first_name': u'alon', 'last_name': u'slotky', 'email': u'alonslotky@yahoo.com', 'password2': u'1234'}, 
         {'first_name': u'alon', 'last_name': u'slotky', 'gender': u'0', 'in_person_tutoring': True, 'zipcode': 1231, 'date_of_birth': datetime.date(1974, 1, 1), 'email': u'alonslotky@yahoo.com', 'online_tutoring': True}, 
         {},
        {'currency': u'3', 'price_per_hour': Decimal('150')}, 
         None]
         {"82618670":{"weekday":"2","begin_hour":6,"begin_minute":15,"end_hour":10,"end_minute":30}}
        '''
        
        #########################################################################
        #  get basic details from Step 1 or from social account ################
        #######################################################################
         
        if is_social_signup:
            
            social_account = self.request.session.get('socialaccount_sociallogin').account
            user = social_account.user
            user.first_name = social_account.extra_data.get('first_name', '')
            user.last_name = social_account.extra_data.get('last_name', '')
            user.email = social_account.extra_data.get('email', '')
            user.username = social_account.extra_data.get('username', '')
            try:
                user.save()
            except Exception, e:
                #TODO render proper response, right?
                import traceback
                traceback.print_exc()
                
                    
        else: #In this case we take the information from the first step form and not from the social account        
            user = User()
            user.is_active = True
            step1_data = form_data[form_data_indices["step1"]]
            user.username = step1_data['email'] 
            user.first_name = step1_data['first_name']
            user.last_name = step1_data['last_name']
            user.email = step1_data['email']
        
            #only used in case the signup is not social
            password = step1_data['password1']
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            
            user.save()
        
        profile = user.profile        
 
        #########################################################################
        #  get additional info from Step 2                      ################
        #######################################################################
        step2_data = form_data[form_data_indices["step2"]]
        profile.gender = step2_data.get('gender', 0)
        profile.timezone = step2_data.get('timezone', None)
        profile.date_of_birth = step2_data.get('date_of_birth')
        profile.zipcode = step2_data.get('zipcode', 0) 
        profile.country = step2_data.get('country', None)
        
        #image handling
        image = None
        session_key = ''

        session_key = self.request.session.session_key
        try:
            image = UploadProfileImage.objects.get(key=session_key).image
        except UploadProfileImage.DoesNotExist:
            pass

        if image:
            profile.profile_image = image
        
        if session_key:
            UploadProfileImage.objects.filter(key=session_key).update(image=None)
            UploadProfileImage.objects.filter(key=session_key).delete()
        
        #########################################################################
        #  get genres from Step 3                               ################
        #######################################################################
        
        self.save_genres(form_list[form_data_indices["step3"]], user)
        
        #########################################################################
        #  get additional info from Step 4                      ################
        #######################################################################
        step4_data = form_data[form_data_indices["step4"]]
        profile.currency = Currency.objects.get(id=step4_data.get('currency', 1))
        profile.price_per_hour = step4_data.get('price_per_hour', -1)
        profile.about = step4_data.get('about', 0)   
        
        #########################################################################
        #  get additional info from Step 5                      ################
        #######################################################################
        step5_data = form_data[form_data_indices["step5"]]
        
        profile.agreement = step5_data.get('agreement', None)
        profile.newsletter = step5_data.get('newsletter', None)
        profile.partners_newsletter = step5_data.get('partners_newsletter', None)
        
        availability_periods = json.loads(step5_data['availability'])
        
        #availability
        for key, val in availability_periods.items():
            #val_example = {"begin_hour":6,"begin_minute":15,"end_hour":10,"end_minute":30}
            availability = WeekAvailability()
            availability.weekday = int(val['weekday'])
            new_object = True
            
            availability.begin = datetime.time(hour = val['begin_hour'], minute = val['begin_minute'])
            availability.end = datetime.time(hour = val['end_hour'], minute = val['end_minute'])
            user.week_availability.add(availability)
        
                
        
        #########################################################################
        #  Wrap Up                                              ################
        #######################################################################
        
        send_email_confirmation(self.request, user)
        
        profile.type = profile.TYPES.TUTOR
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
            print 'Email Template does not exist!'
            pass
          
        return user
    
    def done(self, form_list, **kwargs):
        is_social_signup = bool(self.request.session.get('socialaccount_sociallogin')) #This means social signup was attempted
        
        user = self.save_tutor(form_list, is_social_signup)
        success_url = reverse('edit_tutor_profile')
        
        if is_social_signup:
            sociallogin = self.request.session.get('socialaccount_sociallogin')
            sociallogin.connect(self.request, user)
            return complete_signup(self.request, user, settings.ACCOUNT_EMAIL_VERIFICATION, success_url, signal_kwargs={'sociallogin': sociallogin})
            
                           
        return complete_signup(self.request, user, settings.ACCOUNT_EMAIL_VERIFICATION, success_url)
    
    def get_form_kwargs(self, step):
        if "step2" == step:
            return {"request": self.request}
        else:
            return {}
    def get_form(self, step=None, data=None, files=None):
        
        form = super(TutorSignupWizard, self).get_form(step, data, files)
        
        if type(form) == forms.MultiPartSignupFormStep2:
            if self.request.session.get('socialaccount_sociallogin'):
                
                social_account = self.request.session.get('socialaccount_sociallogin').account
                gender = social_account.extra_data.get('gender', '')
                timezone = social_account.extra_data.get('timezone', '')
                avatar_url = social_account.get_avatar_url()
                birthday = social_account.extra_data.get('birthday', '')
                if avatar_url:
                    
                    image, created = UploadProfileImage.objects.get_or_create(key=self.request.session.session_key)
                    
                    if created:
                        form.fields['avatar_url'].initial = avatar_url
                        
                        #####################################
                        # Save avatar profile image   #
                        #####################################
                        r = requests.get(avatar_url)
                        ext = r.headers['content-type'].split('/')[1] #should be jpeg
                        name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
                        new_filename = '%s.%s' % (name, ext.lower())
                        filename = os.path.join(settings.MEDIA_ROOT, UploadProfileImage.UPLOAD_IMAGES_PATH, new_filename)
                        
                        img_temp = NamedTemporaryFile()
                        img_temp.write(r.content)
                        img_temp.flush()
                        image.image.save(filename, File(img_temp), save=True)
                        
                form.fields['gender'].initial = '0' if gender=='male' else '1'
                if birthday:
                    try:
                        form.fields['date_of_birth'].initial = datetime.datetime.strptime(birthday, '%m/%d/%Y').date()
                    except ValueError:
                        #TODO logger logger
                        print 'Warning: Cannot parse facebook birthday'
                
        

        return form
    
    def get_context_data(self, form, **kwargs):
        context = super(TutorSignupWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'step1':
            context.update({'facebook_app_id': facebook_app_id})
        return context
    
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

def allauth_signup(request, **kwargs):
    
    form_class = kwargs.pop("form_class", SignupForm)
    template_name = kwargs.pop("template_name", "account/signup.html")
    redirect_field_name = kwargs.pop("redirect_field_name", "next")
    success_url = kwargs.pop("success_url", None)
    extra_ctx = kwargs.pop("extra_ctx", {})
    
    if success_url is None:
        success_url = get_login_redirect_url(request, redirect_field_name)
    
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
           "login_url": get_login_redirect_url(request,
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

def socialaccount_signup_wizard(request, *args, **kwargs):
    
    if request.session['socialaccount_sociallogin'].is_existing:
        
        sociallogin = request.session.get('socialaccount_sociallogin')
        return perform_login(request, request.session['socialaccount_sociallogin'].account.user, 'none',
                  redirect_url= reverse('edit_tutor_profile'), signal_kwargs={"sociallogin": sociallogin},
                  signup=False)
    
    #TODO make sure it's tutor signup!
    return redirect('/account/signup/tutor_social/')

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
        print 'socialaccount_signup POST'
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

