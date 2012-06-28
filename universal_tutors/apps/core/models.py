# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Template, Context

from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.model_utils import get_namedtuple_choices

from apps.classes.settings import CREDIT_VALUE
import urlparse, threading

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
	video_id = None
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