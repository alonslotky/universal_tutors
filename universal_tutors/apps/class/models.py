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

from filebrowser.fields import FileBrowseField
from apps.common.utils.fields import AutoOneToOneField, CountryField
from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.geo import geocode_location
from apps.common.utils.model_utils import get_namedtuple_choices


class WeekAvailability(models.Model):
    """
    A tutor week availability
    """
    
    WEEKDAYS = get_namedtuple_choices('WEEKDAYS', (
        (0, 'MONDAY', 'Monday'),
        (1, 'TUESDAY', 'Tuesday'),
        (2, 'WEDNESDAY', 'Wednesday'),
        (3, 'THURSDAY', 'Thursday'),
        (4, 'FRIDAY', 'Friday'),
        (5, 'SATURDAY', 'Saturday'),
        (6, 'SUNDAY', 'Sunday'),
    ))

    user = models.ForeignKey(User, related_name='week_availability')
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAYS.get_choices())
    begin = models.TimeField()
    end = models.TimeField()
    
    def save(self, *args, **kwargs):
        if (self.begin > self.end and self.end.hour!=0) \
            or self.user.week_availability \
                .exclude(Q(id=self.id) | Q(end=self.begin) | Q(begin=self.end)) \
                .filter(Q(weekday=self.weekday), Q(begin__range=(self.begin, self.end)) | Q(end__range=(self.begin, self.end))):
            return
        super(self.__class__, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u'%s (%s from %s to %s)' % (self.user, self.get_weekday_display(), self.begin, self.end)


class DayAvailability(models.Model):
    """
    A custom day availability
    """
    
    user = models.ForeignKey(User, related_name='day_availability')
    date = models.DateField()
    begin = models.TimeField()
    end = models.TimeField()
    dayoff = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if (self.begin > self.end and self.end.hour!=0) \
            or self.user.day_availability \
                .exclude(Q(id=self.id) | Q(end=self.begin) | Q(begin=self.end)) \
                .filter(Q(date=self.date), Q(begin__range=(self.begin, self.end)) | Q(end__range=(self.begin, self.end))):
            return
        super(self.__class__, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u'%s (%s from %s to %s)' % (self.user, self.date, self.begin, self.end)


class Booking(BaseModel):
    """
    Booking chairs from a space on a period of time
    """
    
    BOOKING_STATUS = get_namedtuple_choices('SPACE_COST_TYPES', (
        (0, 'PRE_BOOKED', 'Pre-booked'),
        (1, 'BOOKED', 'Booked'),
        (3, 'CANCELED_BY_USER', 'Canceled by user'),
        (4, 'CANCELED_BY_OWNER', 'Canceled by owner'),
        (5, 'AUTO_CANCELED', 'Auto-canceled'),
    ))

    tutor = models.ForeignKey(User, related_name='classes_as_tutor')
    student = models.ForeignKey(User, related_name='classes_as_student')
    date = models.DateTimeField()
    begin = models.TimeField()
    end = models.TimeField()
    total_fee = models.FloatField()
    tutors_fee = models.FloatField()
    earning_fee = models.FloatField()
    status = models.PositiveSmallIntegerField(choices=BOOKING_STATUS.get_choices(), default=BOOKING_STATUS.PRE_BOOKED)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save()
        user = self.user
        profile = user.profile
        profile.no_booked = user.booking.filter(status = self.BOOKING_STATUS.BOOKED)
        profile.save()

    def __unicode__(self):
        return u'%s (%s from %s to %s)' % (self.space, self.date, self.begin, self.end)

