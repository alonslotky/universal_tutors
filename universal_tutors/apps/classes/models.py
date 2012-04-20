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

import re, unicodedata, random, string, datetime, os
from scribblar import rooms

from filebrowser.fields import FileBrowseField
from apps.common.utils.fields import AutoOneToOneField, CountryField
from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.geo import geocode_location
from apps.common.utils.model_utils import get_namedtuple_choices

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
    
    
class Class(BaseModel):
    """
    A class object
    """
    class Meta:
        verbose_name_plural = 'Classes'
    
    tutor = models.ForeignKey(User, related_name='classes_as_tutor')
    student = models.ForeignKey(User, related_name='classes_as_student')
    subject = models.ManyToManyField(ClassSubject, related_name='classes')
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    credit_fee = models.FloatField()
    scribblar_id = models.CharField(max_length = 100, null=True, blank=True)
    
    name = models.CharField(max_length = 100)
    
    def save(self, *args, **kwargs):
        is_new = not self.id
        super(self.__class__, self).save()
        
        if is_new:
            scribblar_room = rooms.add(
                roomname = self.name,
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
            rooms.edit(roomid=self.scribblar_id, roomname=self.name)
    
    def lock(self):
        rooms.edit(roomid=self.scribblar_id, locked='1')
    
    def __unicode__(self):
        return self.name


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

