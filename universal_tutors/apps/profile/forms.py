from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.contrib.formtools.wizard import FormWizard

from uni_form.helpers import FormHelper, Submit, Reset, Button
from uni_form.helpers import Layout, Fieldset, Row, HTML, Div

from allauth.account.app_settings import *
from allauth.account.forms import LoginForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.account.utils import user_display, perform_login, send_email_confirmation
from allauth.utils import email_address_exists

from apps.classes.models import *
from apps.classes.settings import MINIMUM_CREDITS_PER_HOUR
from apps.common.utils.form_fields import ListField
from apps.common.utils.fields import COUNTRIES
from apps.profile.models import *
from apps.core.models import Currency, EmailTemplate, Country, Timezone

import urllib2
import urlparse
import simplejson
from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.forms import *

###for mptt subjects############
from itertools import chain
from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from apps.profile.fmpttforms import *

class MPTTModelChoiceIterator(forms.models.ModelChoiceIterator):
    def choice(self, obj):
        tree_id = getattr(obj, getattr(self.queryset.model._meta, 'tree_id_atrr', 'tree_id'), 0)
        left = getattr(obj, getattr(self.queryset.model._meta, 'left_atrr', 'lft'), 0)
        return super(MPTTModelChoiceIterator, self).choice(obj) + ((tree_id, left),)


class MPTTModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        level = getattr(obj, getattr(self.queryset.model._meta, 'level_attr', 'level'), 0)
        return u'%s %s' % ('-'*level, smart_unicode(obj))
    
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return MPTTModelChoiceIterator(self)
    
    choices = property(_get_choices, forms.ChoiceField._set_choices)


class MPTTFilteredSelectMultiple(widgets.FilteredSelectMultiple):
    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        super(MPTTFilteredSelectMultiple, self).__init__(verbose_name, is_stacked, attrs, choices)
    
    def render_options(self, choices, selected_choices):
        """
        this is copy'n'pasted from django.forms.widgets Select(Widget)
        change to the for loop and render_option so they will unpack and use our extra tuple of mptt sort fields
        (if you pass in some default choices for this field, make sure they have the extra tuple too!)
        """
        def render_option(option_value, option_label, sort_fields):
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            return u'<option value="%s" data-tree-id="%s" data-left-value="%s"%s>%s</option>' % (
                escape(option_value),
                sort_fields[0],
                sort_fields[1],
                selected_html,
                conditional_escape(force_unicode(option_label)),
            )
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label, sort_fields in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label, sort_fields))
        return u'\n'.join(output)
    
    class Media:
        extend = False
        js = (settings.ADMIN_MEDIA_PREFIX + "js/core.js",
              settings.MEDIA_URL + "js/mptt_m2m_selectbox.js",
              settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js",
              )


class TutorSubjectForm(forms.ModelForm):
    class Meta:
        models = TutorSubject
        fields = ('system', 'level', 'subject', 'credits')
    
    def clean_credits(self):
        credits = self.cleaned_data['credits']
        if credits < MINIMUM_CREDITS_PER_HOUR:
            raise forms.ValidationError(_(u'Minimum %s credits per hour' % MINIMUM_CREDITS_PER_HOUR))
        return credits
        
        
class StudentInterestForm(forms.ModelForm):
    class Meta:
        models = StudentInterest
        fields = ('subject', 'system', 'level')


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    account_email = forms.EmailField()
    password  = forms.CharField(label=_('Password'), min_length = 5, max_length = 30, widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(label=_('New Password'), min_length = 5, max_length = 30, widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label=_('Repeat password'), min_length = 5, max_length = 30, widget=forms.PasswordInput, required=False)

    class Meta:
        fields = ('about', 'video', 'date_of_birth', 'country', 'timezone', 'gender', 
                  'profile_image', 'crb', 'crb_file', 'currency', 'webcam', 'paypal_email',
                  'notifications_messages', 'notifications_classes', 'notifications_other',)
        model = UserProfile
        widgets = {
            'profile_image': forms.FileInput(),
            'country': forms.Select(attrs = {'class': 'stretch'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['country'].required = True
        # self.fields['webcam'].help_text = 'Users will need atleast a 500kbps internet connection in order to use the classroom functionality'


    def clean_account_email(self):
        email = self.cleaned_data['account_email']
        user_id = self.instance.user.id if self.instance else 0 
        if User.objects.filter(email=email).exclude(id=user_id).count() > 0:
            raise forms.ValidationError(_(u"This email is already registered."))
        return email
    
    def clean(self):
        cleaned_data = self.cleaned_data

        passwd  = cleaned_data.get('password', '')
        passwd1 = cleaned_data.get('password1', None)
        passwd2 = cleaned_data.get('password2', None)
        
        video = cleaned_data.get('video', None)
        
        if video:
            video_id = None
            try:
                parsed = urlparse.urlparse(video)
                video_id = urlparse.parse_qs(parsed.query)['v'][0]
            except IndexError:
                if video.find('http://youtu.be/') > 0:
                    video_id = video.replace('http://youtu.be/', '')
            except KeyError:
                if video.find('http://youtu.be/') > 0:
                    video_id = video.replace('http://youtu.be/', '')                
                
            if not video_id:
                self._errors['video'] = self.error_class([_(u'Please provide a valid video url.')])
                
            else:                    
                response = urllib2.urlopen('http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % video_id)
                response = response.read()
                data = simplejson.loads(response)
                
                duration = int(data['entry']['media$group']['yt$duration']['seconds'])
    
                if duration > 60:
                    self._errors['video'] = self.error_class([_(u'Your video has exceeded the 60 seconds limit.')])

        if passwd1 or passwd2:
            user = self.instance.user
            if not user.check_password(passwd):
                self._errors['password'] = self.error_class([_(u'Password is invalid')])
            elif passwd1 != passwd2:
                self._errors['password1'] = self.error_class([_(u'Passwords should match')])
            else:
                user.set_password(passwd1)

        return cleaned_data
    
TutorSubjectFormSet = inlineformset_factory(User, TutorSubject, form=TutorSubjectForm)
TutorQualificationFormSet = inlineformset_factory(User, TutorQualification)
StudentInterestFormSet = inlineformset_factory(User, StudentInterest, form=StudentInterestForm)
    


class SigninForm(LoginForm):
    helper = FormHelper()
    helper.form_tag = False
    email = forms.CharField()

    layout = Layout(
        Fieldset('',
            'email',
            'password',
        ),
    )

    helper.add_layout(layout)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = ''

    def user_credentials(self):
        """
        Provides the credentials required to authenticate the username for
        login.
        """
        
        credentials = {}
        credentials["username"] = self.cleaned_data["email"]
        credentials["password"] = self.cleaned_data["password"]
 
        return credentials
    
    def email_credentials(self):
        """
        Provides the credentials required to authenticate the email for
        login.
        """
        
        credentials = {}
        credentials["email"] = self.cleaned_data["email"]
        credentials["password"] = self.cleaned_data["password"]
 
        return credentials
    
    def clean(self):
        if self._errors:
            return
        
        user = authenticate(**self.user_credentials())
        if not user: user = authenticate(**self.email_credentials())

        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is currently inactive."))
        else:
            raise forms.ValidationError(_("The login details you specified are not correct."))

        return self.cleaned_data


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )
        
    username = forms.SlugField(label=_('Username'), min_length=5, max_length=25, initial='')
    first_name = forms.CharField(label=_('First name'), max_length = 25, initial='')
    last_name = forms.CharField(label=_('Last name'), max_length = 25, initial='')
    email = forms.EmailField(label=_('Email'), max_length = 255, initial='')
    password1 = forms.CharField(label=_('Password'), min_length = 5, max_length = 30, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Repeat password'), min_length = 5, max_length = 30, widget=forms.PasswordInput)
    
    #Adding the zipcode attribute 
    zipcode = forms.CharField(label=_('zipcode'), min_length = 5, max_length = 10, initial='') 
    country = forms.ChoiceField(label=_('Country'), choices=COUNTRIES, widget=forms.Select(attrs={'class': 'stretch'}))
    date_of_birth = forms.DateField(label=_('Date of birth'), initial='')

    gender = forms.ChoiceField(label=_('Gender'), choices=UserProfile.GENDER_TYPES.get_choices(), widget=forms.Select(attrs={'class': 'stretch'}))
    timezone = forms.ChoiceField(label=_('Timezone'), choices=[(tz, tz) for tz in pytz.all_timezones], widget=forms.Select(attrs={'class': 'stretch'}), initial='UTC')
    
    referral = forms.ChoiceField(label=_('Referral'), choices=[('', 'Please select an option')]+UserProfile.REFERRAL_TYPES.get_choices(), widget=forms.Select(attrs={'class': 'stretch'}))
    referral_other = forms.CharField(required = False, initial='')
    referral_key = forms.CharField(required = False, initial='')

    agreement = forms.BooleanField(required = False, help_text='I have read and accepted the Terms and Conditions from the box above.')
    newsletter = forms.BooleanField(required = False, initial=True, help_text="I don't mind receiving occasional newsletters from Universal Tutors with offers and other news.")
    partners_newsletter = forms.BooleanField(required = False, initial=True, help_text="I don't mind receiving occasional emails from carefully selected partners of Universal Tutors")
    
    online_tutoring = forms.BooleanField(required = True, initial=True)
    in_person_tutoring = forms.BooleanField(required = True, initial=True)
        
    def clean_agreement(self):
        agreement = self.cleaned_data.get('agreement', False)
        if not agreement:
            raise forms.ValidationError(_(u"You need to agree with terms and conditions to Sign Up."))
        
        return agreement
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).count() > 0:
            raise forms.ValidationError(_(u"This username is already used."))

        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(_(u"This email is already registered."))

        return email

    def clean_password2(self):
        passwd1 = self.cleaned_data['password1']
        passwd2 = self.cleaned_data['password2']
        if passwd1 != passwd2:
            raise forms.ValidationError(_(u'Passwords should match'))

        return passwd1

    def clean(self):
        cleaned_data = self.cleaned_data
        referral = int(self.cleaned_data.get('referral', 0))
        referral_other = self.cleaned_data.get('referral_other', None)
        if referral == UserProfile.REFERRAL_TYPES.OTHER and not referral_other:
            self._errors['referral_other'] = self.error_class(['Please specify how you learned about us.'])

        return cleaned_data

    def save(self, commit=True, request=None):
        image = None
        session_key = ''
        if request:
            session_key = request.session.session_key
            try:
                image = UploadProfileImage.objects.get(key=session_key).image
            except UploadProfileImage.DoesNotExist:
                pass
            
        user = super(SignupForm, self).save(commit=False)

        password = self.cleaned_data['password1']
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.is_active = True
        user.save()
        
        profile = user.profile        
        profile.country = self.cleaned_data['country']
        profile.referral = int(self.cleaned_data.get('referral', 0))
        profile.other_referral = self.cleaned_data.get('referral_other', None)
        profile.referral_key = self.cleaned_data.get('referral_key', None)
        profile.gender = self.cleaned_data.get('gender', 0)
        profile.newsletters = self.cleaned_data.get('newsletter', False)
        profile.partners_newsletters = self.cleaned_data.get('partners_newsletter', None)
        profile.timezone = self.cleaned_data.get('timezone', None)
        profile.currency = Currency.objects.get(id=self.cleaned_data.get('currency', 1))
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.zipcode = self.cleaned_data.get('zipcode', 0)    

        if image:
            profile.profile_image = image

        if self.parent:
            user.parent_set.create(parent=self.parent, active=True)
            profile.type = profile.TYPES.UNDER16

        profile.crb = self.cleaned_data.get('crb', False)
        profile.save()
        
        if session_key:
            UploadProfileImage.objects.filter(key=session_key).update(image=None)
            UploadProfileImage.objects.filter(key=session_key).delete()        
        
        send_email_confirmation(user, request=request)
        
        return user

    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent', None)
        super(SignupForm, self).__init__(*args, **kwargs)
        if self.parent:
            self.fields['date_of_birth'].required = False
        

class StudentSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(StudentSignupForm, self).__init__(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        request = kwargs.get('request')
        user = super(StudentSignupForm, self).save(*args, **kwargs)
        profile = user.profile

        for i in range(0, 13):
            try:
                subject = ClassSubject.objects.get(id = request.POST.get('interests-%s-subject' % i, 0) or 0)
            except ClassSubject.DoesNotExist:
                subject = None

            try:
                system = EducationalSystem.objects.get(id = request.POST.get('interests-%s-system' % i, 0) or 0)
            except EducationalSystem.DoesNotExist:
                system = None
            
            try:
                level = ClassLevel.objects.get(id = request.POST.get('interests-%s-level' % i, 0) or 0)
            except ClassLevel.DoesNotExist:
                level = None
        
            if subject:
                user.interests.create(subject=subject, system=system, level=level)

        profile.type = profile.TYPES.STUDENT
        profile.save()
        
        return user


class Under16SignupForm(StudentSignupForm):
    def save(self, *args, **kwargs):
        user = super(Under16SignupForm, self).save(*args, **kwargs)
        profile = user.profile

        profile.type = profile.TYPES.UNDER16
        profile.save()
        
        return user


class ParentSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(ParentSignupForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        user = super(ParentSignupForm, self).save(*args, **kwargs)
        profile = user.profile
        profile.type = profile.TYPES.PARENT
        profile.save()
        
        return user

class MultiPartSignupFormStep1(forms.Form):
    class Meta:
        model = User
        #fields = ('username', 'first_name', 'last_name', 'email')
    
    #Do we have username in the first one???
    #username = forms.SlugField(label=_('Username'), min_length=5, max_length=25, initial='')
    first_name = forms.CharField(label=_('First name'), max_length = 25, initial='')
    last_name = forms.CharField(label=_('Last name'), max_length = 25, initial='')
    email = forms.EmailField(label=_('Email'), max_length = 255, initial='')
    password1 = forms.CharField(label=_('Password'), min_length = 5, max_length = 30, widget=forms.PasswordInput)
    #password2 = forms.CharField(label=_('Repeat password'), min_length = 5, max_length = 30, widget=forms.PasswordInput)

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if User.objects.filter(username__iexact=username).count() > 0:
#             raise forms.ValidationError(_(u"This username is already used."))
# 
#         return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(_(u"This email is already registered."))

        return email

    #def clean_password2(self):
        #passwd1 = self.cleaned_data['password1']
        #passwd2 = self.cleaned_data['password2']
        #if passwd1 != passwd2:
            #raise forms.ValidationError(_(u'Passwords should match'))

        #return passwd1




class MultiPartSignupFormStep2(forms.Form):
    class Meta:
        model = User
        fields = ('date_of_birth', 'gender', 'zipcode',)
        
    #first_name = forms.CharField(label=_('First name'), max_length = 25, initial='', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #last_name = forms.CharField(label=_('Last name'), max_length = 25, initial='', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #email = forms.EmailField(label=_('Email'), max_length = 255, initial='', widget=forms.TextInput(attrs={'readonly':'readonly', 'disabled':True}))
    
    #Adding the zipcode attribute 
    zipcode = forms.CharField(label=_('zipcode'), min_length = 5, max_length = 10, initial='') 
    #online_tutoring = forms.BooleanField(required = True, initial=True)
    #in_person_tutoring = forms.BooleanField(required = True, initial=True)
    
    date_of_birth = forms.DateField(label=_('Date of birth'), initial='')
    gender = forms.ChoiceField(label=_('Gender'), choices=UserProfile.GENDER_TYPES.get_choices(), widget=forms.Select(attrs={'class': 'stretch'}))
    country = forms.ChoiceField(label=_('Country'), choices=COUNTRIES, widget=forms.Select(attrs={'class': 'stretch'}),initial='US')
    timezone = forms.ChoiceField(label=_('Timezone'), choices=[(tz, tz) for tz in pytz.all_timezones], widget=forms.Select(attrs={'class': 'stretch'}), initial='US/Eastern')
     
 

#<<<<<<< HEAD
#=======
    image_uploaded = forms.BooleanField(required = False)
    
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(MultiPartSignupFormStep2, self).__init__(*args, **kwargs)

         
    def clean_image_uploaded(self):
        session_key = self.request.session.session_key
        
        try:
            image = UploadProfileImage.objects.get(key=session_key).image
        except UploadProfileImage.DoesNotExist:
            raise forms.ValidationError(_(u"Please upload a profile picture"))


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(_(u"This email is already registered."))

        return email
#>>>>>>> 6177e35764a2302c59bf57ca80721f38909eedfd
    
class MultiPartSignupFormStep3(forms.Form):
    
    
    cat=range(0,Genre.tree.filter(level=0).count())
    for x in range(0, len(cat)):
        cat[x]=Genre.tree.filter(level=0)[x]

    subcat=[None]*len(cat)
    for x in range(0, len(cat)):
        subcat[x]=cat[x].get_children()
        
    genres = forms.ModelMultipleChoiceField(queryset= Genre.objects.all(), widget=forms.CheckboxSelectMultiple, required = False)

    genre_0_0=forms.ModelMultipleChoiceField(queryset=cat[0].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_1_0=forms.ModelMultipleChoiceField(queryset=cat[1].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_1_1=forms.ModelMultipleChoiceField(queryset=cat[1].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_1_2=forms.ModelMultipleChoiceField(queryset=cat[1].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_1_3=forms.ModelMultipleChoiceField(queryset=cat[1].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    

    genre_2_0=forms.ModelMultipleChoiceField(queryset=cat[2].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_2_1=forms.ModelMultipleChoiceField(queryset=cat[2].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_3_0=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_3_1=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_3_2=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_3_3=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_3_4=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[4].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_3_5=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[5].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_3_6=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[6].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    
    genre_4_0=forms.ModelMultipleChoiceField(queryset=cat[4].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_4_1=forms.ModelMultipleChoiceField(queryset=cat[4].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_4_2=forms.ModelMultipleChoiceField(queryset=cat[4].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_5_0=forms.ModelMultipleChoiceField(queryset=cat[5].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_5_1=forms.ModelMultipleChoiceField(queryset=cat[5].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_5_2=forms.ModelMultipleChoiceField(queryset=cat[5].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
        

    genre_6_0=forms.ModelMultipleChoiceField(queryset=cat[6].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_6_1=forms.ModelMultipleChoiceField(queryset=cat[6].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_7_0=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_1=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_2=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_3=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_4=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[4].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_5=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[5].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_6=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[6].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_7=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[7].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_8=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[8].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_9=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[9].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_10=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[10].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_11=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[11].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_12=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[12].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_13=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[13].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_14=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[14].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_15=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[15].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_16=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[16].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_17=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[17].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_18=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[18].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_19=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[19].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_20=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[20].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_21=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[21].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_22=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[22].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_23=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[23].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_7_24=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[24].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_8_0=forms.ModelMultipleChoiceField(queryset=cat[8].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_8_1=forms.ModelMultipleChoiceField(queryset=cat[8].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_8_2=forms.ModelMultipleChoiceField(queryset=cat[8].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_8_3=forms.ModelMultipleChoiceField(queryset=cat[8].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_9_0=forms.ModelMultipleChoiceField(queryset=cat[9].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_10_0=forms.ModelMultipleChoiceField(queryset=cat[10].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_11_0=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_11_1=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_11_2=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_11_3=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_11_4=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[4].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_12_0=forms.ModelMultipleChoiceField(queryset=cat[12].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_12_1=forms.ModelMultipleChoiceField(queryset=cat[12].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_12_2=forms.ModelMultipleChoiceField(queryset=cat[12].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_12_3=forms.ModelMultipleChoiceField(queryset=cat[12].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    genre_13_0=forms.ModelMultipleChoiceField(queryset=cat[13].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    

    genre_14_0=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_1=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_2=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_3=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_4=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[4].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_5=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[5].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_6=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[6].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_7=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[7].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_8=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[8].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_9=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[9].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_10=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[10].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_11=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[11].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_12=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[12].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_13=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[13].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_14=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[14].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    genre_14_15=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[15].get_children(),widget=forms.CheckboxSelectMultiple, required=False)
    
    


class MultiPartSignupFormStep4(forms.Form):
    class Meta:
        model = User
        #fields = ('profile.currency')
        
    price_per_hour = forms.DecimalField(initial=0)
    about = forms.CharField(label=_('Description'), initial='')
    currency = forms.ChoiceField(choices=[(currency.id, '%s - %s' % (currency.acronym, currency.name)) for currency in Currency.objects.all()])
    
    tutoring_type = forms.MultipleChoiceField(label=_('Type of Tutoring*'), choices=UserProfile.TUTORING_TYPES.get_choices(), widget=forms.CheckboxSelectMultiple, initial=[0,1],
                                              help_text = 'We are in the process of adding in-person tutoring as a feature on wizoku. Please tick as many boxes as apply (you can always edit this later) and we will let you know once this feature is up and running')
    
    
class MultiPartSignupFormStep5(forms.Form):
    class Meta:
        model = User
        
    default_week = [('Monday', 0, []), ('Tuesday', 1, []), ('Wednesday', 2, []), ('Thursday', 3, []), ('Friday', 4, []), ('Saturday', 5, []), ('Sunday', 6, [])]
    availability = forms.CharField(widget=forms.HiddenInput())
    agreement = forms.BooleanField(required = True, help_text='I have read and accepted the Terms and Conditions from the box above.')
    newsletter = forms.BooleanField(required = False, initial=True, help_text="I don't mind receiving occasional newsletters from Universal Tutors with offers and other news.")
    partners_newsletter = forms.BooleanField(required = False, initial=True, help_text="I don't mind receiving occasional emails from carefully selected partners of Universal Tutors")
    
    def clean_agreement(self):
        agreement = self.cleaned_data.get('agreement', False)
        if not agreement:
            raise forms.ValidationError(_(u"You need to agree with terms and conditions to Sign Up."))
        
        return agreement    
    
class MultiPartSignupFormStep6(forms.ModelForm):
    class Meta:
        model = User

class TutorSignupForm(SignupForm):
    about = forms.CharField(label=_('Description'), initial='')
    crb = forms.BooleanField(label='I have a CRB', required=False)
    webcam = forms.BooleanField(label='I have a WebCam', required=False)#, help_text='Users will need at least a 500kbps internet connection in order to use the classroom functionality')
    currency = forms.ChoiceField(choices=[(currency.id, '%s - %s' % (currency.acronym, currency.name)) for currency in Currency.objects.all()])
    paypal_email = forms.EmailField(label=_('PayPal Email'), max_length = 255, initial='', required=False)
    cat=range(0,Genre.tree.filter(level=0).count())
    for x in range(0, len(cat)):
        cat[x]=Genre.tree.filter(level=0)[x]

    subcat=[None]*len(cat)
    for x in range(0, len(cat)):
        subcat[x]=cat[x].get_children()

    genre_0_0=forms.ModelMultipleChoiceField(queryset=cat[0].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_1_0=forms.ModelMultipleChoiceField(queryset=cat[1].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_1_1=forms.ModelMultipleChoiceField(queryset=cat[1].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_1_2=forms.ModelMultipleChoiceField(queryset=cat[1].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_1_3=forms.ModelMultipleChoiceField(queryset=cat[1].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple)
    

    genre_2_0=forms.ModelMultipleChoiceField(queryset=cat[2].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_2_1=forms.ModelMultipleChoiceField(queryset=cat[2].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_3_0=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_3_1=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_3_2=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_3_3=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_3_4=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[4].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_3_5=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[5].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_3_6=forms.ModelMultipleChoiceField(queryset=cat[3].get_children()[6].get_children(),widget=forms.CheckboxSelectMultiple)
    
    
    genre_4_0=forms.ModelMultipleChoiceField(queryset=cat[4].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_4_1=forms.ModelMultipleChoiceField(queryset=cat[4].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_4_2=forms.ModelMultipleChoiceField(queryset=cat[4].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_5_0=forms.ModelMultipleChoiceField(queryset=cat[5].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_5_1=forms.ModelMultipleChoiceField(queryset=cat[5].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_5_2=forms.ModelMultipleChoiceField(queryset=cat[5].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
        

    genre_6_0=forms.ModelMultipleChoiceField(queryset=cat[6].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_6_1=forms.ModelMultipleChoiceField(queryset=cat[6].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_7_0=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_1=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_2=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_3=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_4=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[4].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_5=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[5].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_6=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[6].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_7=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[7].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_8=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[8].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_9=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[9].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_10=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[10].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_11=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[11].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_12=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[12].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_13=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[13].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_14=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[14].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_15=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[15].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_16=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[16].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_17=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[17].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_18=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[18].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_19=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[19].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_20=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[20].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_21=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[21].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_22=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[22].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_23=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[23].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_7_24=forms.ModelMultipleChoiceField(queryset=cat[7].get_children()[24].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_8_0=forms.ModelMultipleChoiceField(queryset=cat[8].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_8_1=forms.ModelMultipleChoiceField(queryset=cat[8].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_8_2=forms.ModelMultipleChoiceField(queryset=cat[8].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_8_3=forms.ModelMultipleChoiceField(queryset=cat[8].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_9_0=forms.ModelMultipleChoiceField(queryset=cat[9].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_10_0=forms.ModelMultipleChoiceField(queryset=cat[10].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_11_0=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_11_1=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_11_2=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_11_3=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_11_4=forms.ModelMultipleChoiceField(queryset=cat[11].get_children()[4].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_12_0=forms.ModelMultipleChoiceField(queryset=cat[12].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_12_1=forms.ModelMultipleChoiceField(queryset=cat[12].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_12_2=forms.ModelMultipleChoiceField(queryset=cat[12].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_12_3=forms.ModelMultipleChoiceField(queryset=cat[12].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple)
    
    genre_13_0=forms.ModelMultipleChoiceField(queryset=cat[13].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    

    genre_14_0=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[0].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_1=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[1].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_2=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[2].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_3=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[3].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_4=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[4].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_5=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[5].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_6=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[6].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_7=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[7].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_8=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[8].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_9=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[9].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_10=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[10].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_11=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[11].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_12=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[12].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_13=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[13].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_14=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[14].get_children(),widget=forms.CheckboxSelectMultiple)
    genre_14_15=forms.ModelMultipleChoiceField(queryset=cat[14].get_children()[15].get_children(),widget=forms.CheckboxSelectMultiple)
    


        
   

    def __init__(self, *args, **kwargs):
        super(TutorSignupForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TutorSignupForm, self).clean()
        crb = cleaned_data.get('crb', False)
        return cleaned_data
            
    def save(self, *args, **kwargs):
        user = super(TutorSignupForm, self).save(*args, **kwargs)
        profile = user.profile
        profile.about = self.cleaned_data.get('about', '')
        profile.crb = self.cleaned_data.get('crb', False)
        profile.webcam = self.cleaned_data.get('webcam', False)
        profile.type = profile.TYPES.TUTOR
        profile.paypal_email = self.cleaned_data.get('paypal_email', None)
        profile.tutoring_type = self.cleaned_data.get('tutoring_type', 0)
        pofile.genre_0_0= self.cleaned_data.get('genre_0_0',0)
        pofile.genre_1_0= self.cleaned_data.get('genre_1_0',0)
        pofile.genre_1_1= self.cleaned_data.get('genre_1_1',0)
        pofile.genre_1_2= self.cleaned_data.get('genre_1_2',0)
        pofile.genre_1_3= self.cleaned_data.get('genre_1_3',0)
        pofile.genre_2_0= self.cleaned_data.get('genre_2_0',0)
        pofile.genre_2_1= self.cleaned_data.get('genre_2_1',0)
        pofile.genre_3_0= self.cleaned_data.get('genre_3_0',0)
        pofile.genre_3_1= self.cleaned_data.get('genre_3_1',0)
        pofile.genre_3_2= self.cleaned_data.get('genre_3_2',0)
        pofile.genre_3_3= self.cleaned_data.get('genre_3_3',0)
        pofile.genre_3_4= self.cleaned_data.get('genre_3_4',0)
        pofile.genre_3_5= self.cleaned_data.get('genre_3_5',0)
        pofile.genre_3_6= self.cleaned_data.get('genre_3_6',0)
        pofile.genre_4_0= self.cleaned_data.get('genre_4_0',0)
        pofile.genre_4_1= self.cleaned_data.get('genre_4_1',0)
        pofile.genre_4_2= self.cleaned_data.get('genre_4_2',0)
        pofile.genre_4_3= self.cleaned_data.get('genre_4_3',0)
        pofile.genre_5_0= self.cleaned_data.get('genre_5_0',0)
        pofile.genre_5_1= self.cleaned_data.get('genre_5_1',0)
        pofile.genre_5_2= self.cleaned_data.get('genre_5_2',0)
        pofile.genre_6_0= self.cleaned_data.get('genre_6_0',0)
        pofile.genre_6_1= self.cleaned_data.get('genre_6_1',0)
        pofile.genre_7_1= self.cleaned_data.get('genre_7_1',0)
        pofile.genre_7_2= self.cleaned_data.get('genre_7_2',0)
        pofile.genre_7_3= self.cleaned_data.get('genre_7_3',0)
        pofile.genre_7_4= self.cleaned_data.get('genre_7_4',0)
        pofile.genre_7_5= self.cleaned_data.get('genre_7_5',0)
        pofile.genre_7_6= self.cleaned_data.get('genre_7_6',0)
        pofile.genre_7_7= self.cleaned_data.get('genre_7_7',0)
        pofile.genre_7_8= self.cleaned_data.get('genre_7_8',0)
        pofile.genre_7_9= self.cleaned_data.get('genre_7_9',0)
        pofile.genre_7_10= self.cleaned_data.get('genre_7_10',0)
        pofile.genre_7_11= self.cleaned_data.get('genre_7_11',0)
        pofile.genre_7_12= self.cleaned_data.get('genre_7_12',0)
        pofile.genre_7_13= self.cleaned_data.get('genre_7_13',0)
        pofile.genre_7_14= self.cleaned_data.get('genre_7_14',0)
        pofile.genre_7_15= self.cleaned_data.get('genre_7_15',0)
        pofile.genre_7_16= self.cleaned_data.get('genre_7_16',0)
        pofile.genre_7_17= self.cleaned_data.get('genre_7_17',0)
        pofile.genre_7_18= self.cleaned_data.get('genre_7_18',0)
        pofile.genre_7_19= self.cleaned_data.get('genre_7_19',0)
        pofile.genre_7_20= self.cleaned_data.get('genre_7_20',0)
        pofile.genre_7_21= self.cleaned_data.get('genre_7_21',0)
        pofile.genre_7_22= self.cleaned_data.get('genre_7_22',0)
        pofile.genre_7_23= self.cleaned_data.get('genre_7_23',0)
        pofile.genre_7_24= self.cleaned_data.get('genre_7_24',0)
        pofile.genre_7_25= self.cleaned_data.get('genre_7_25',0)
        pofile.genre_8_0= self.cleaned_data.get('genre_8_0',0)
        pofile.genre_8_1= self.cleaned_data.get('genre_8_1',0)
        pofile.genre_8_2= self.cleaned_data.get('genre_8_2',0)
        pofile.genre_8_3= self.cleaned_data.get('genre_8_3',0)
        pofile.genre_9_0= self.cleaned_data.get('genre_9_0',0)
        pofile.genre_10_0= self.cleaned_data.get('genre_10_0',0)
        pofile.genre_11_0= self.cleaned_data.get('genre_11_0',0)
        pofile.genre_11_1= self.cleaned_data.get('genre_11_1',0)
        pofile.genre_11_2= self.cleaned_data.get('genre_11_2',0)
        pofile.genre_11_3= self.cleaned_data.get('genre_11_3',0)
        pofile.genre_11_4= self.cleaned_data.get('genre_11_4',0)
        pofile.genre_12_0= self.cleaned_data.get('genre_12_0',0)
        pofile.genre_12_1= self.cleaned_data.get('genre_12_1',0)
        pofile.genre_12_2= self.cleaned_data.get('genre_12_2',0)
        pofile.genre_12_3= self.cleaned_data.get('genre_12_3',0)
        pofile.genre_13_1= self.cleaned_data.get('genre_13_1',0)
        pofile.genre_14_0= self.cleaned_data.get('genre_14_0',0)
        pofile.genre_14_1= self.cleaned_data.get('genre_14_1',0)
        pofile.genre_14_2= self.cleaned_data.get('genre_14_2',0)
        pofile.genre_14_3= self.cleaned_data.get('genre_14_3',0)
        pofile.genre_14_4= self.cleaned_data.get('genre_14_4',0)
        pofile.genre_14_5= self.cleaned_data.get('genre_14_5',0)
        pofile.genre_14_6= self.cleaned_data.get('genre_14_6',0)
        pofile.genre_14_7= self.cleaned_data.get('genre_14_7',0)
        pofile.genre_14_8= self.cleaned_data.get('genre_14_8',0)
        pofile.genre_14_9= self.cleaned_data.get('genre_14_9',0)
        pofile.genre_14_10= self.cleaned_data.get('genre_14_10',0)
        pofile.genre_14_11= self.cleaned_data.get('genre_14_11',0)
        pofile.genre_14_12= self.cleaned_data.get('genre_14_12',0)
        pofile.genre_14_13= self.cleaned_data.get('genre_14_13',0)
        pofile.genre_14_14= self.cleaned_data.get('genre_14_14',0)
        pofile.genre_14_15= self.cleaned_data.get('genre_14_15',0)
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
    

class NewsletterSubscribeForm(forms.Form):
    email = forms.EmailField(required=True)


class EditProfileForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length = 25)
    last_name = forms.CharField(label=_('Last name'), max_length = 25)
    email = forms.EmailField(label=_('Email'), max_length = 255)

    title = forms.CharField(label=_('Profile Title'), max_length = 100, required=False)
    about = forms.CharField(label=_('Summary'), widget=forms.Textarea(attrs={'cols': 54}), required=False)
    address = forms.CharField(label=_('Address'), max_length=150, required=False)
    location = forms.CharField(label=_('Location'), max_length=50, required=False)
    postcode = forms.CharField(label=_('Postcode'), max_length=10, required=False)
    country = forms.ChoiceField(label=_('Country'), choices=COUNTRIES)


    # helper = FormHelper()

    # helper.form_tag = False
    # layout = Layout(
    #     Fieldset('',
    #              'first_name',
    #              'last_name',
    #              'title',
    #              'email',
    #              'country', 'location',
    #              'about',
    #     ),
    # )

    # helper.add_layout(layout)

class ProfilePhotoForm(forms.Form):
    photo = forms.ImageField()

    helper = FormHelper()
        
    helper.form_tag = False
    layout = Layout(
        Fieldset('',
            'photo',
        ),
    )
    helper.add_layout(layout)

    # Submit button(s)
    button = Button('cancel','Cancel', css_class='secondaryAction')
    helper.add_input(button)
    submit = Submit('submit','Import', css_class='primaryAction')
    helper.add_input(submit)


class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ('name', 'email')



class GenericSocialSignupForm(SocialSignupForm):
    country = forms.ChoiceField(label=_('Country'), choices=COUNTRIES, widget=forms.Select(attrs={'class': 'stretch'}))
    date_of_birth = forms.DateField(label=_('Date of birth'), initial='')

    gender = forms.ChoiceField(label=_('Gender'), choices=UserProfile.GENDER_TYPES.get_choices(), widget=forms.Select(attrs={'class': 'stretch'}))
    timezone = forms.ChoiceField(label=_('Timezone'), choices=[(tz, tz) for tz in pytz.all_timezones], widget=forms.Select(attrs={'class': 'stretch'}))
    
    referral = forms.ChoiceField(label=_('Referral'), choices=UserProfile.REFERRAL_TYPES.get_choices(), widget=forms.Select(attrs={'class': 'stretch'}))
    referral_other = forms.CharField(required = False, initial='')
    referral_key = forms.CharField(required = False, initial='')

    agreement = forms.BooleanField(required = False, help_text='I have read and accepted the Terms and Conditions from the box above.')
    newsletter = forms.BooleanField(required = False, initial=True, help_text="I don't mind receiving occasional newsletters from Universal Tutors with offers and other news.")
    partners_newsletter = forms.BooleanField(required = False, initial=True, help_text="I don't mind receiving occasional emails from carefully selected partners of Universal Tutors")

    def clean_agreement(self):
        agreement = self.cleaned_data.get('agreement', False)
        if not agreement:
            raise forms.ValidationError(_(u"You need to agree with terms and conditions to Sign Up."))
        
        return agreement
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(_(u"This username is already used."))

        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(_(u"This email is already registered."))

        return email

    def clean(self):
        cleaned_data = self.cleaned_data
        referral = int(self.cleaned_data.get('referral', 0))
        referral_other = self.cleaned_data.get('referral_other', None)
        if referral == UserProfile.REFERRAL_TYPES.OTHER and not referral_other:
            self._errors['referral_other'] = self.error_class(['Please specify how you learned about us.'])

        return cleaned_data


    def save(self, request=None):
        image = None
        session_key = ''
        if request:
            session_key = request.session.session_key
            try:
                image = UploadProfileImage.objects.get(key=session_key).image
            except UploadProfileImage.DoesNotExist:
                pass

        user = super(GenericSocialSignupForm, self).save(request)
        profile = user.profile
        profile.country = self.cleaned_data['country']
        profile.referral = int(self.cleaned_data.get('referral', 0))
        profile.other_referral = self.cleaned_data.get('referral_other', None)
        profile.referral_key = self.cleaned_data.get('referral_key', None)
        profile.gender = self.cleaned_data.get('gender', 0)
        profile.newsletters = self.cleaned_data.get('newsletter', False)
        profile.partners_newsletters = self.cleaned_data.get('partners_newsletter', False)
        profile.timezone = self.cleaned_data.get('timezone', None)
        profile.currency = Currency.objects.get(id=self.cleaned_data.get('currency', 1))
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.crb = self.cleaned_data.get('crb', False)

        if image:
            profile.profile_image = image

        profile.save()
        
        if session_key:
            UploadProfileImage.objects.filter(key=session_key).update(image=None)
            UploadProfileImage.objects.filter(key=session_key).delete()        

        return user


class TutorSocialSignupForm(GenericSocialSignupForm):
    about = forms.CharField(label=_('Description'), initial='')
    crb = forms.BooleanField(label='I have a CRB', required=False)
    webcam = forms.BooleanField(label='I have a WebCam', required=False)#, help_text='Users will need at least a 500kbps internet connection in order to use the classroom functionality')
    currency = forms.ChoiceField(choices=[(currency.id, '%s - %s' % (currency.acronym, currency.name)) for currency in Currency.objects.all()])

    def save(self, request=None):
        user = super(TutorSocialSignupForm, self).save(request)
        profile = user.profile
        profile.about = self.cleaned_data.get('about', '')
        profile.crb = self.cleaned_data.get('crb', False)
        profile.webcam = self.cleaned_data.get('webcam', False)
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
            pass

        return user

class StudentSocialSignupForm(GenericSocialSignupForm):

    def save(self, request=None):
        user = super(StudentSocialSignupForm, self).save(request)
        profile = user.profile
        
        for i in range(0, 13):
            try:
                subject = ClassSubject.objects.get(id = request.POST.get('interests-%s-subject' % i, 0) or 0)
            except ClassSubject.DoesNotExist:
                subject = None

            try:
                system = EducationalSystem.objects.get(id = request.POST.get('interests-%s-system' % i, 0) or 0)
            except EducationalSystem.DoesNotExist:
                system = None
            
            try:
                level = ClassLevel.objects.get(id = request.POST.get('interests-%s-level' % i, 0) or 0)
            except ClassLevel.DoesNotExist:
                level = None
        
            if subject:
                user.interests.create(subject=subject, system=system, level=level)
#                    
#        for title in list_new_subjects:
#            try:
#                subject = ClassSubject.objects.get(subject__iexact = title)
#            except ClassSubject.DoesNotExist:
#                subject = ClassSubject(subject = title)
#            subject.save()
#            profile.interests.add(subject)
            
        profile.type = profile.TYPES.STUDENT
        profile.save()

        return user

class ParentSocialSignupForm(GenericSocialSignupForm):

    def save(self, request=None):
        user = super(ParentSocialSignupForm, self).save(request)
        profile = user.profile
        profile.type = profile.TYPES.PARENT
        profile.save()

        return user


#class Genre(SignupForm): 
    ##cat=range(0,Genre.tree.filter(level=0).count())
    #for x in range(0, len(cat)):
        cat[x]=Genre.tree.filter(level=0)[x]

    #subcat=[None]*len(cat)
    #for x in range(0, len(cat)):
        #subcat[x]=cat[x].get_children()
