# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Template, Context
from django.contrib.auth.models import User

from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.model_utils import get_namedtuple_choices
from apps.common.utils.fields import CountryField

from apps.classes.settings import CREDIT_VALUE
import urlparse, threading, string, random, datetime


class Currency(BaseModel):
    class Meta:
        verbose_name_plural = 'Currencies'
    
    acronym = models.CharField(max_length=3, help_text='Example: GBP')
    name = models.CharField(max_length=25, help_text='Example: British pound')
    symbol = models.CharField(max_length=3, help_text='Example: £')
    value = models.FloatField(help_text='One to GBP')
    manual = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s' % (self.acronym, self.name)
    
    def credit_value(self):
        return CREDIT_VALUE * self.value


class Quote(models.Model):
    quote = models.TextField()
    
    def __unicode__(self):
        return self.quote


class Video(models.Model):
    
    VIDEO_TYPES = get_namedtuple_choices('VIDEO_TYPES', (
        (0, 'HOME', 'Home'),
        (1, 'TUTORGUIDE', 'Tutor Guide'),
        (2, 'STUDENTGUIDE', 'Student Guide'),
    ))
    
    description = models.CharField(max_length=30)
    url = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    type = models.PositiveSmallIntegerField(choices=VIDEO_TYPES.get_choices())

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.active:
            Video.objects.filter(active=True, type=self.type).exclude(id = self.id).update(active = False)
        super(self.__class__, self).save(*args, **kwargs)

    def get_video_id(self):
        try:
            parsed = urlparse.urlparse(self.url)
            video_id = urlparse.parse_qs(parsed.query)['v'][0]
        except IndexError:
            if self.url.find('http://youtu.be/') > 0:
                video_id = self.url.replace('http://youtu.be/', '')
        except KeyError:
            if self.url.find('http://youtu.be/') > 0:
                video_id = self.url.replace('http://youtu.be/', '')
        return video_id


class Bundle(models.Model):
    """
    Package with discounts
    """
    class Meta:
        ordering = ('credits', )
    
    credits = models.FloatField()
    discount = models.FloatField(help_text='Type 0.05 to 5% of discount')
    
    def __unicode__(self):
        return '%s' % self.credits
    
    def get_discount_percentage(self):
        return '%s' % (self.discount * 100)
    

class Discount(BaseModel):
    """
    Create discount code and roles
    """
    
    TYPES = get_namedtuple_choices('USER_TYPE', (
        (0, 'ALL', 'All users'),
        (1, 'TUTOR', 'Tutors'),
        (2, 'STUDENT', 'Students'),
        (3, 'PARENT', 'Parents'),
    ))
    
    type = models.PositiveSmallIntegerField(choices=TYPES.get_choices())
    description = models.CharField(max_length=255, null=True, blank=True, help_text='Optional. Just to internal identification')
    code = models.SlugField(max_length=15, null=True, blank=True, unique=True, db_index=True, help_text='We recommend more than 6 chars. To auto-generation left this field empty')
    start = models.DateField(help_text='Date at this discount starts')
    end = models.DateField(help_text='Date at this discount ends')
    valid = models.PositiveSmallIntegerField(help_text="Number of times this discount can be used by an user. Type 0 for unlimited.")

    discount_percentage = models.FloatField(help_text="A percentage. Example: 0.10 for 10% discount on top-up for student; 10% deducted from UT commission at the end of class for tutors")
    discount_fixed = models.FloatField(help_text="A fixed number of credits. Example: additional 10 credits on top-up for a student; 10 credits deducted from UT commission at the end of class for a tutor")

    def __unicode__(self):
        return self.description if self.description else self.code

    def is_valid(self, used=0):
        today = datetime.date.today()
        return (self.start <= today <= self.end) and (not self.valid or used <= self.valid)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        super(Discount, self).save(*args, **kwargs)
            

class DiscountUser(BaseModel):
    """
    Users who used discount
    """
    class Meta:
        unique_together = ('user', 'discount')

    user = models.ForeignKey(User, related_name='discounts')
    discount = models.ForeignKey(Discount, related_name='users')
    used = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s: %s' % (self.discount, self.user.get_full_name())
    
    def is_valid(self):
        valid = self.discount.is_valid(self.used)
        if not valid:
            self.active = False
            super(DiscountUser, self).save()
        return valid

    def use(self):
        self.used += 1
        super(DiscountUser, self).save()
        self.is_valid()
        

# EMAIL TEMPLATES
from apps.profile.models import UserProfile as _UserProfile

class EmailTemplate(models.Model):
    type = models.PositiveSmallIntegerField(choices=_UserProfile.NOTIFICATIONS_TYPES.get_choices(), unique=True, db_index=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    
    
    def __unicode__(self):
        return self.get_type_display()
    
    
    def send_email(self, context, to_email, use_thread=True):
        template = Template(self.body)
        c = Context(context) 
        html = template.render(c)
        
        sender = 'Universal Tutors <%s>' % settings.DEFAULT_FROM_EMAIL
                    
        email_message = EmailMessage(self.subject, html, sender, to_email)
        email_message.content_subtype = 'html'
            
        if use_thread:
            t = threading.Thread(target=email_message.send, kwargs={'fail_silently': False})
            t.setDaemon(True)
            t.start()
        else:
            email_message.send()


#### TIMEZONE #############################################################
class Timezone(models.Model):    
    class Meta:
        ordering = ['timezone']
        
    timezone = models.CharField(max_length=100, unique=True, db_index=True)

    def __unicode__(self):
        return self.timezone

class Country(models.Model):
    class Meta:
        verbose_name = 'Country and timezones'
        ordering = ['country_name']
        
    country = CountryField(unique=True, db_index=True)
    country_name = models.CharField(max_length=150)
    timezones = models.ManyToManyField(Timezone, null=True, blank=True)

    def list_timezones(self):
        return ', '.join([t.timezone for t in self.timezones.all()])
            
    def __unicode__(self):
        return self.country_name

