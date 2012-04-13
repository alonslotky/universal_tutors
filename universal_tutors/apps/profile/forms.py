from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from uni_form.helpers import FormHelper, Submit, Reset, Button
from uni_form.helpers import Layout, Fieldset, Row, HTML, Div

from allauth.account.app_settings import *
from allauth.account.forms import LoginForm
from allauth.account.utils import user_display, perform_login, send_email_confirmation
from allauth.utils import email_address_exists

from apps.common.utils.fields import COUNTRIES
from apps.profile.models import UserProfile



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ()

        widgets = {
            'photo': forms.FileInput(),
        }
        

    helper = FormHelper()
        
    helper.form_tag = False
    layout = Layout(
        Fieldset('',
            'first_name',
            'last_name',
        ),
    )

    helper.add_layout(layout)


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
    first_name = forms.CharField(label=_('First name'), max_length = 25, initial='')
    last_name = forms.CharField(label=_('Last name'), max_length = 25, initial='')
    email = forms.EmailField(label=_('Email'), max_length = 255, initial='')
    password1 = forms.CharField(label=_('Password'), min_length = 5, max_length = 30, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Repeat password'), min_length = 5, max_length = 30, widget=forms.PasswordInput)

    address = forms.CharField(label=_('Address'), max_length=150, initial='')
    location = forms.CharField(label=_('Location'), max_length=50, initial='')
    postcode = forms.CharField(label=_('Postcode'), max_length=10, initial='')
    country = forms.ChoiceField(label=_('Country'), choices=COUNTRIES)
    date_of_birth = forms.DateField(label=_('Date of birth'), initial='')
    type = forms.IntegerField(label=_('Type'), initial='')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(_(u"This email already registered."))

        return email

    def clean_password2(self):
        passwd1 = self.cleaned_data['password1']
        passwd2 = self.cleaned_data['password2']
        if passwd1 != passwd2:
            raise forms.ValidationError(_(u'Passwords should match'))

        return passwd1

    def save(self, commit=True, request=None):
        user = super(SignupForm, self).save(commit=False)
        if not user.username:
            user_id = User.objects.latest('id').id
            while True:
                user_id += 1
                user.username = 'user%05d' % user_id
                try:
                    User.objects.get(username__iexact=user.username)
                except User.DoesNotExist:
                    break
        
        password = self.cleaned_data['password1']
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.is_active = False    
        user.save()

        profile = user.profile        
        profile.address = self.cleaned_data['address']
        profile.location = self.cleaned_data['location']
        profile.postcode = self.cleaned_data['postcode']
        profile.country = self.cleaned_data['country']
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.type = self.cleaned_data['type']
        profile.save()
        
        send_email_confirmation(user, request=request)
        
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


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
