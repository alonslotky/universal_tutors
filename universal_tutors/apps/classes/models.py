from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.template import loader, Context
from django.core.urlresolvers import reverse

import re, unicodedata, random, string, datetime, os, pytz
from scribblar import rooms

from filebrowser.fields import FileBrowseField
from apps.common.utils.fields import AutoOneToOneField, CountryField
from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.geo import geocode_location
from apps.common.utils.model_utils import get_namedtuple_choices
from apps.common.utils.date_utils import add_minutes_to_time, first_day_of_week, minutes_difference, minutes_to_time
from apps.classes.settings import *

class ClassSubject(models.Model):
    """
    A class type
    """
    class Meta:
        verbose_name_plural = 'Subject'
        verbose_name_plural = 'Subjects'
    
    subject = models.CharField(max_length = 30)
    
    def __unicode__(self):
        return self.subject
    
    
class ClassError(Exception): pass
class Class(BaseModel):
    """
    A class object
    """
    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ('status', 'date', 'start')

    STATUS_TYPES = get_namedtuple_choices('STATUS_TYPES', (
        (0, 'PRE_BOOKED', 'Pre-booked'),
        (1, 'BOOKED', 'BOOKED'),
        (2, 'DONE', 'Done'),
        (2, 'CANCELED_BY_STUDENT', 'Canceled by the student'),
        (3, 'CANCELED_BY_TUTOR', 'Canceled by the tutor'),
        (4, 'CANCELED_BY_SYSTEM', 'Canceled by the system'),
    ))
    
    tutor = models.ForeignKey(User, related_name='classes_as_tutor')
    student = models.ForeignKey(User, related_name='classes_as_student')
    subject = models.ForeignKey(ClassSubject, related_name='classes')
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    credit_fee = models.FloatField()
    earning_fee = models.FloatField()
    universal_fee = models.FloatField()
    scribblar_id = models.CharField(max_length = 100, null=True, blank=True)
    
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES.get_choices(), default=STATUS_TYPES.PRE_BOOKED)
    
    def save(self, *args, **kwargs):
        tutor = self.tutor
        tutor_profile = tutor.profile
        tutor_subject = tutor.subjects.filter(subject=self.subject)
        if tutor_subject and tutor_profile.check_period(self.date, self.start, self.end):
            self.total_fee = tutor_subject[0].credits * (minutes_difference(self.end, self.start) / 60.0)
            self.earning_fee = self.total_fee * (1 - UNIVERSAL_FEE)
            self.cotton_fee = self.total_fee * UNIVERSAL_FEE

            is_new = not self.id
            super(self.__class__, self).save(*args, **kwargs)
        
            if is_new:
                scribblar_room = rooms.add(
                    roomname = '%s' % self.subject,
                    roomowner = self.tutor.profile.get_scribblar_id(),
                    promoteguests = '0',
                    allowguests = '0',
                    clearassets = '0',
                    enablehistory = '1',
                    whitelabel = '1',
                    roomaudio = '1',
                    roomvideo = '1',
                    roomchat = '1',
                    roomwolfram = '1',
                    hideheader = '1',
                    hideflickr = '1',
                    hidestamp = '0',
                    autostartcam = '1',
                    autostartaudio = '1',
                    allowrecord = '1',
                    map = '0',
                    locked = '0',
                    allowlock = '0',
                )
                
                self.scribblar_id = scribblar_room['roomid']
                super(self.__class__, self).save()
            else:
                rooms.edit(roomid=self.scribblar_id, roomname='%s' % self.subject)
    
    def delete(self):
        rooms.delete(roomid=self.scribblar_id)
        
    def __unicode__(self):
        return '%s' % self.subject

    def get_start(self):
        from django.utils.timezone import utc        
        self.start.replace(tzinfo=utc)
        return self.start

    def get_end(self):
        return self.end.tzname()
    
    def cancel_by_tutor(self):
        if self.status == self.STATUS_TYPES.BOOKED:
            self.status = self.STATUS_TYPES.CANCELED_BY_TUTOR
            super(self.__class__, self).save()
            rooms.delete(roomid=self.scribblar_id)
    
    def cancel_by_student(self):
        if self.status == self.STATUS_TYPES.BOOKED:
            self.status = self.STATUS_TYPES.CANCELED_BY_STUDENT
            super(self.__class__, self).save()
            rooms.delete(roomid=self.scribblar_id)

    def done(self):
        if self.status == self.STATUS_TYPES.BOOKED:
            self.status = self.STATUS_TYPES.DONE
            super(self.__class__, self).save()
            rooms.edit(roomid=self.scribblar_id, locked='1')

class ClassUserHistory(models.Model):
    """
    A class history object
    """
    
    _class = models.ForeignKey(Class, related_name='history')
    user = models.ForeignKey(User, related_name='class_history')
    enter = models.DateTimeField(auto_now_add = True)
    leave = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return '%s [%s]: from %s to %s' % (self.user, self._class, self.enter, self.leave)

