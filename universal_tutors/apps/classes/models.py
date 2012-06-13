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
from django.core.exceptions import ObjectDoesNotExist


import re, unicodedata, random, string, datetime, os, pytz
from scribblar import rooms, assets, recordings

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
        ordering = ('status', 'date')

    STATUS_TYPES = get_namedtuple_choices('STATUS_TYPES', (
        (0, 'PRE_BOOKED', 'Pre-booked'),
        (1, 'BOOKED', 'BOOKED'),
        (2, 'DONE', 'Done'),
        (3, 'CANCELED_BY_STUDENT', 'Canceled by the student'),
        (4, 'CANCELED_BY_TUTOR', 'Canceled by the tutor'),
        (5, 'CANCELED_BY_SYSTEM', 'Canceled by the system'),
        (6, 'STOPPED_BY_STUDENT', 'Stopped by the student'),
    ))
    
    RESPONSE_TYPES = get_namedtuple_choices('STATUS_TYPES', (
        (0, 'CONTINUE', 'Continue'),
        (1, 'ASK_TO_CONTINUE', 'Ask to continue'),
        (2, 'CLOSE_ALERT', 'Close alert'),
        (3, 'CLOSE', 'Close'),
    ))
    
    
    tutor = models.ForeignKey(User, related_name='classes_as_tutor')
    student = models.ForeignKey(User, related_name='classes_as_student')
    subject = models.ForeignKey(ClassSubject, related_name='classes')
    date = models.DateTimeField()
    duration = models.PositiveSmallIntegerField()
    credit_fee = models.FloatField()
    earning_fee = models.FloatField()
    universal_fee = models.FloatField()
    scribblar_id = models.CharField(max_length = 100, null=True, blank=True)
    cancelation_reason = models.CharField(max_length = 500, null=True, blank=True)
    
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES.get_choices(), default=STATUS_TYPES.PRE_BOOKED)
    alert_sent = models.BooleanField(False)
    
    def get_updated_credit_fee(self, commit=True):
        tutor = self.tutor
        tutor_profile = tutor.profile
        tutor_subject = tutor.subjects.filter(subject=self.subject)
        is_new = not self.id
        
        if tutor_subject and tutor_profile.check_period(self.date, self.start, self.end):
            self.credit_fee = tutor_subject[0].credits * (minutes_difference(self.end, self.start) / 60.0)
            self.earning_fee = self.credit_fee * (1 - UNIVERSAL_FEE)
            self.universal_fee = self.credit_fee * UNIVERSAL_FEE
            if commit:
                super(self.__class__, self).save(*args, **kwargs)

        return self.credit_fee
    
    
    def save(self, *args, **kwargs):
        tutor = self.tutor
        tutor_profile = tutor.profile
        tutor_subject = tutor.subjects.filter(subject=self.subject)
        is_new = not self.id
        
        if is_new:
            if tutor_subject and tutor_profile.check_period(self.date, self.start, self.start + datetime.timedelta(minutes=self.duration), gtz=pytz.utc):
                self.credit_fee = tutor_subject[0].credits * (minutes_difference(self.end, self.start) / 60.0)
                self.earning_fee = self.credit_fee * (1 - UNIVERSAL_FEE)
                self.universal_fee = self.credit_fee * UNIVERSAL_FEE
    
                super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)                
            if self.scribblar_id:
                try:
                    rooms.edit(roomid=self.scribblar_id, roomname='%s' % self.subject)
                except:
                    self.create_scribblar_class()
    
    def create_scribblar_class(self):
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
    from scribblar import assets

    def delete(self):
        if self.scribblar_id:
            try:
                rooms.delete(roomid=self.scribblar_id)
            except:
                pass
        super(self.__class__, self).delete()
        
    def __unicode__(self):
        return '%s' % self.subject

    def get_start(self):
        from django.utils.timezone import utc        
        self.start.replace(tzinfo=utc)
        return self.start

    def get_end(self):
        return self.end.tzname()
    
    def canceled_by_tutor(self, reason):
        if self.status == self.STATUS_TYPES.BOOKED:
            self.status = self.STATUS_TYPES.CANCELED_BY_TUTOR
            self.cancelation_reason = reason
            super(self.__class__, self).save()
            rooms.delete(roomid=self.scribblar_id)

            from apps.profile.models import UserCreditMovement
            student = self.student
            student_profile = student.profile
            student_profile.credit += self.credit_fee
            student_profile.save()
            student.movements.create(type=UserCreditMovement.MOVEMENTS_TYPES.CANCELED_BY_TUTOR, credits=self.credit_fee)
            student_profile.send_notification(student_profile.NOTIFICATIONS_TYPES.CANCELED_BY_TUTOR, {
                'class': self,
                'student': student,
                'tutor': self.tutor,
            })

    def stop_class(self):
        if self.status == self.STATUS_TYPES.BOOKED:
            self.status = self.STATUS_TYPES.STOPPED_BY_STUDENT
            super(self.__class__, self).save()
            rooms.delete(roomid=self.scribblar_id)

            from apps.profile.models import UserCreditMovement
            student = self.student
            student_profile = student.profile
            student_profile.credit += self.credit_fee
            student_profile.save()
            student.movements.create(type=UserCreditMovement.MOVEMENTS_TYPES.STOPPED_BY_STUDENT, credits=self.credit_fee)

    def canceled_by_student(self, reason):
        if self.status == self.STATUS_TYPES.BOOKED:
            self.status = self.STATUS_TYPES.CANCELED_BY_STUDENT
            self.cancelation_reason = reason
            super(self.__class__, self).save()
            rooms.delete(roomid=self.scribblar_id)
            
            from apps.profile.models import UserCreditMovement
            student = self.student
            student_profile = student.profile
            student_profile.credit += self.credit_fee
            student_profile.save()
            student.movements.create(type=UserCreditMovement.MOVEMENTS_TYPES.CANCELED_BY_STUDENT, credits=self.credit_fee)
            tutor = self.tutor
            tutor_profile = tutor.profile
            tutor_profile.classes_given = tutor.classes_as_tutor.filter(status=self.STATUS_TYPES.DONE).count()
            tutor_profile.save()
            tutor_profile.send_notification(tutor_profile.NOTIFICATIONS_TYPES.CANCELED_BY_STUDENT, {
                'class': self,
                'student': student,
                'tutor': tutor,
            })

    def alert(self):
        student = self.student
        tutor = self.tutor
        tutor_profile = tutor.profile
        tutor_profile.send_notification(tutor_profile.NOTIFICATIONS_TYPES.CLASS, {
            'class': self,
            'student': student,
            'tutor': tutor,
        })
        tutor_profile = tutor.profile
        tutor_profile.send_notification(tutor_profile.NOTIFICATIONS_TYPES.CLASS, {
            'class': self,
            'student': student,
            'tutor': tutor,
        })
        self.alert_sent = True
        super(self.__class__, self).save()

    def done(self):
        if self.status == self.STATUS_TYPES.BOOKED:
            self.status = self.STATUS_TYPES.DONE
            super(self.__class__, self).save()
            rooms.edit(roomid=self.scribblar_id, locked='1')

            from apps.profile.models import UserCreditMovement, Referral

            tutor = self.tutor
            try:
                referral = Referral.objects.filter(user = tutor, used=False, activated=True).latest('id')
                referral.used = True
                referral.save()
                with_referral = True
            except Referral.DoesNotExist:
                with_referral = False
                pass
            tutor_profile = tutor.profile
            tutor_profile.income += self.earning_fee if not with_referral else self.credit_fee
            tutor_profile.classes_given = tutor.classes_as_tutor.filter(status=self.STATUS_TYPES.DONE).count() 
            tutor_profile.save()
            tutor.movements.create(type=UserCreditMovement.MOVEMENTS_TYPES.INCOME, credits=self.credit_fee)
            tutor_profile.send_notification(tutor_profile.NOTIFICATIONS_TYPES.INCOME, {
                'class': self,
                'student': self.student,
                'tutor': tutor,
            })
            
            for referral in Referral.objects.select_related().filter(Q(key=tutor_profile.key) | Q(key=self.user.profile.key), Q(used=False)):
                user = referral.user
                profile = user.profile
                count = user.referrals.filter(user=user, done=True).count()
                if count < 3:
                    if profile.type == profile.TYPES.STUDENT or profile.type == profile.TYPES.UNDER16:
                        profile.credit += 5
                        profile.save()
                        referral.used = True 
                    elif profile.type == profile.TYPES.TUTOR:
                        referral.activated = True
                else:
                   referral.used = True 
                referral.save()

    def book(self):
        tutor = self.tutor
        tutor_profile = tutor.profile
        student = self.student
        student_profile = student.profile
        if self.status == self.STATUS_TYPES.PRE_BOOKED and student_profile.credit >= self.credit_fee:
            self.status = self.STATUS_TYPES.BOOKED
            super(self.__class__, self).save()
            self.create_scribblar_class()
            
            from apps.profile.models import UserCreditMovement
            student_profile.credit -= self.credit_fee
            student_profile.save()
            student.movements.create(type=UserCreditMovement.MOVEMENTS_TYPES.PAYMENT, credits=self.credit_fee)
            tutor_profile.send_notification(tutor_profile.NOTIFICATIONS_TYPES.BOOKED, {
                'class': self,
                'student': student,
                'tutor': tutor,
            })
    
    def tutor_rating(self):
        try:
            return self.tutor.reviews_as_tutor.filter(related_class = self).latest('id')
        except ObjectDoesNotExist:
            return None

    def student_rating(self):
        try:
            return self.student.reviews_as_student.filter(related_class = self).latest('id')
        except ObjectDoesNotExist:
            return None
    
    def get_material(self):
        return assets.list(roomid=self.scribblar_id)
    
    def get_recordings(self):
        return recordings.listbyroom(roomid=self.scribblar_id)
    
    def download(self, id):
        return assets.url(assetid=id, client=143)
    
    def get_rec_url(self, id):
        return recordings.url(recid=id)

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

