from django.db import models
from django.db.models import Q
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

from filebrowser.fields import FileBrowseField
from apps.common.utils.fields import AutoOneToOneField, CountryField
from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.geo import geocode_location
from apps.common.utils.model_utils import get_namedtuple_choices
from apps.common.utils.date_utils import add_minutes_to_time, first_day_of_week, minutes_difference, minutes_to_time

from apps.classes.models import Class, ClassSubject
from apps.classes.settings import *

from scribblar import users

class UserProfile(BaseModel):
    """
    Profile and configurations for a user
    """
    DEFAULT_PHOTO = 'images/default/profile.png'

    TYPES = get_namedtuple_choices('USER_TYPE', (
        (0, 'NONE', 'NOT DEFINED'),
        (1, 'TUTOR', 'Tutor'),
        (2, 'STUDENT', 'Student'),
        (3, 'PARENT', 'Parent'),
        (4, 'UNDER16', 'Under-16 Student'),
    ))

    GENDER_TYPES = get_namedtuple_choices('USER_TYPE', (
        (0, 'MALE', 'Male'),
        (1, 'FEMALE', 'Female'),
    ))

    REFERRAL_TYPES = get_namedtuple_choices('USER_REFERRAL_TYPES', (
        (0, 'NONE', 'None'),
        (1, 'FACEBOOK', 'Facebook'),
        (2, 'TWITTER', 'Twitter'),
        (3, 'GOOGLE', 'Google+'),
        (20, 'OTHER', 'Other'),
    ))

    
    def get_upload_to(instance, filename):
        name, ext = os.path.splitext(filename)
        name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
        new_filename = '%s%s' % (name, ext.lower())
        return os.path.join('uploads/profiles/profile_images', new_filename)

    user = AutoOneToOneField(User, related_name="profile")
    
    about = models.CharField(verbose_name=_('About'), max_length=500, null=True, blank=True)
    title = models.CharField(verbose_name=_('Title'), max_length=100, null=True, blank=True)
    profile_image = models.ImageField(verbose_name=_('Profile image'), upload_to=get_upload_to, default=settings.DEFAULT_PROFILE_IMAGE)
    address = models.CharField(verbose_name=_('Address'), max_length=150, null=True, blank=True)
    location = models.CharField(verbose_name=_('Location'), max_length=50, null=True, blank=True)
    postcode = models.CharField(verbose_name=_('Postcode'), max_length=10, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    phone = models.CharField(verbose_name=_('Phone number'), max_length=20, null=True, blank=True)
    newsletters = models.BooleanField(verbose_name=_('Newsletters'))
    date_of_birth = models.DateField(verbose_name=_('Date of birth'), null=True, blank=True)
    scribblar_id = models.CharField(verbose_name=_('Scribblar ID'), max_length=100, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(verbose_name=_('Gender'), choices=GENDER_TYPES.get_choices(), default=GENDER_TYPES.MALE)
    timezone = models.CharField(verbose_name=_('Phone Timezone'), max_length=50, default=pytz.tz)
    
    video = models.CharField(verbose_name=_('Video'), max_length=200, null=True, blank=True)

    type = models.PositiveSmallIntegerField(choices=TYPES.get_choices(), default=TYPES.NONE)
    credit = models.FloatField(default=0)
    income = models.FloatField(default=0)

    referral = models.PositiveSmallIntegerField(choices=REFERRAL_TYPES.get_choices(), default=TYPES.NONE)

    # tutor
    avg_rate = models.FloatField(default=0)

    @property
    def is_over16(self):
        if not self.date_of_birth:
            return False
        
        today = datetime.date.today()        
        # there are no problem because 29 Feb less 16 years it's 29 Feb too
        date = datetime.date(today.year - 16, today.month, today.day)

        return self.date_of_birth <= date

    @property
    def parent(self):
        if not self.date_of_birth:
            return None

        today = datetime.date.today()        
        # there are no problem because 29 Feb less 16 years it's 29 Feb too
        date = datetime.date(today.year - 16, today.month, today.day)

        if self.date_of_birth <= date:
            return self
        
        try:
            return self.parent_set.filter(active=True).latest('id')
        except Child.DoesNotExist:
            return None

    def __unicode__(self):
        user = self.user
        if user.first_name:
            return u'%s %s' % (user.first_name, user.last_name)

        return user.username

    def __update_location(self):
        location = ''
        if self.address:
            location = '%s,' % self.address
        if self.location:
            location = '%s %s,' % (location, self.location) 
        location = '%s %s' % (location, self.get_country_display())
        self.latitude, self.longitude = geocode_location(location)
        super(self.__class__, self).save()
    
    def save(self, *args, **kwargs):
        if self.type != self.TYPES.NONE and not self.is_over16:
            self.type = self.TYPES.UNDER16
        super(self.__class__, self).save(*args, **kwargs)

        if self.type != self.TYPES.NONE and self.type != self.TYPES.PARENT:
            user = self.user
            users.edit(
                userid = self.get_scribblar_id(),
                firstname = user.first_name,
                lastname = user.last_name,
                email = user.email,
                roleid = 50 if self.type == self.TYPES.TUTOR else 10,
            )
                                
        self.__update_location()

    def get_profile_image_path(self):
        return self.profile_image.path if self.profile_image else os.path.join(settings.MEDIA_ROOT, self.DEFAULT_PHOTO)

    def get_social_accounts(self):
        return self.user.socialaccount_set.all()

    def update_information(self, form):
        data = form.cleaned_data
        user = self.user
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.save()

    def update_tutor_information(self, form):
        self.update_information(form)
        data = form.cleaned_data
        user = self.user        

    def check_day(self, date=None):
        available, list = self.get_day(date)
        return available

    def get_day(self, date=None):
        """
        Get availability from a day
        """        
        return self.get_period(date)

    def check_week(self, date=None, begin=None, end=None):
        available, list = self.get_day(date, begin, end)
        return available

    def get_week(self, date=None):
        """
        Get availability from a week
        """
        date = date if date else datetime.date.today()
        date = date - datetime.timedelta(days=date.weekday())
        
        get_day = self.get_day
        week_availability = [get_day(date + datetime.timedelta(days=dt)) for dt in xrange(0,7)]
        
        all_week_available = True
        for element in week_availability:
            if not element[0]:
                all_week_available = False
                break
        
        return (all_week_available, week_availability)    
        

    def check_period(self, date=None, begin=None, end=None):
        available, list = self.get_day(date, begin, end)
        return all([slot[1]-slot[2] > 0 for slot in list])

    def get_period(self, date=None, begin=None, end=None):
        """
        Get availability from a period of time
        
        Return a tuple with boolean and a list of lists: (all_slots_available, [[time, total_availability, booked], ...])
        all_slots_available - True if all slots on this period are available
        """
        user = self.user

        now = datetime.datetime.now()
        date = date if date else now.date()
        begin = begin if begin else datetime.time(0,0)
        end = end if end else datetime.time(0,0)
        all_slots_available = True
        
        weekday = date.weekday()
        begin_of_week = date - datetime.timedelta(days = weekday)
        
        
        midnight = datetime.time(0,0)

        # select availability from date
        availability = user.day_availability.filter(date=date)
        if not availability:

            # select availability from a default week
            availability = user.week_availability.filter(weekday = weekday)
            if not availability:
                all_slots_available = False
                
        # select booking from date
        booking = self.classes_as_tutor.filter(Q(status=Booking.BOOKING_STATUS.BOOKED), Q(date=date) | Q(date=begin_of_week, type=Booking.BOOKING_TYPES.WEEK))

        size = 0
        availability_by_time = []
        append = availability_by_time.append
        time = datetime.datetime.combine(date, begin)
        
        # create empty available array
        while (end==midnight and time!=midnight) or (end!=midnight and time<end) or not size:
            append([[time.hour, time.minute], 0, 0])
            time = add_minutes_to_time(time, MINIMUM_PERIOD)
            size += 1

        # inject total availability on array
        for period in availability:
            start_index = (period.begin.hour - begin.hour) * PERIOD_STEPS + (period.begin.minute / MINIMUM_PERIOD)
            if period.end.hour != 0:
                end_index = (period.end.hour - begin.hour) * PERIOD_STEPS + (period.end.minute / MINIMUM_PERIOD)
            else:
                end_index = size

            # cut index outside the array
            if start_index < 0:     start_index = 0
            if start_index > size:  start_index = size
            if end_index < 0:       end_index = 0
            if end_index > size:    end_index = size
            
            for index in xrange(start_index, end_index+1):
                availability_by_time[index][1] = 1 if not period.dayoff else 0
                

        # inject booking on array
        for item in booking:
            start_index = (item.begin.hour - begin.hour) * PERIOD_STEPS + (item.begin.minute / MINIMUM_PERIOD)
            if item.end.hour != 0:
                end_index = (item.end.hour - begin.hour) * PERIOD_STEPS + (item.end.minute / MINIMUM_PERIOD)
            else:
                end_index = size
            
            # cut index outside the array
            if start_index < 0:     start_index = 0
            if start_index > size:  start_index = size
            if end_index < 0:       end_index = 0
            if end_index > size:    end_index = size

            for index in xrange(start_index, end_index+1):
                availability_by_time[index][2] = 1
                if availability_by_time[index][1] <= availability_by_time[index][2]:
                    all_slots_available = False
        
        return (all_slots_available, availability_by_time)

    def get_default_week(self):
        WEEKDAYS = WeekAvailability.WEEKDAYS.get_choices()
        week = [(WEEKDAYS[weekday][1], weekday, []) for weekday in range(7)]

        for a in self.user.week_availability.all():
            week[a.weekday][2].append(a)
    
        return week

    def get_first_photo(self):
        return self.photos.all()[0].photo.path if self.photos.all() else os.path.join(settings.MEDIA_ROOT, self.DEFAULT_PHOTO)

    def get_scribblar_id(self):
        if not self.scribblar_id:
            user = self.user
            scribblar_user = users.add(
                username = user.username,
                firstname = user.first_name,
                lastname = user.last_name,
                email = user.email,
                roleid = 50 if self.type == self.TYPES.TUTOR else 10,
            )
            self.scribblar_id = scribblar_user['userid']
            super(self.__class__, self).save()
        
        return self.scribblar_id


### TUTOR ###########
class TutorSubject(models.Model):
    user = models.ForeignKey(User, related_name='subjects')
    subject = models.ForeignKey(ClassSubject, related_name='tutors')
    credits = models.FloatField()
    
    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return '%s' % self.subject


class TutorQualification(models.Model):
    def get_upload_to(instance, filename):
        name, ext = os.path.splitext(filename)
        name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
        new_filename = '%s%s' % (name, ext.lower())
        return os.path.join('uploads/profiles/qualifications/documents', new_filename)

    user = models.ForeignKey(User, related_name='qualifications')
    qualification = models.CharField(max_length=200)
    document = models.FileField(null=True, blank=True, upload_to=get_upload_to)
        
    def __unicode__(self):
        return self.qualification

class TutorReview(BaseModel):
    user = models.ForeignKey(User, related_name='reviews')
    rate = models.PositiveSmallIntegerField(default = 0)
    text = models.TextField()
    
    def save(self, *args, **kwargs):
        user = self.user
        super(self.__class__, self).save(*args, **kwargs)
        profile = user.profile
        profile.avg_rate = user.reviews.aggregate(avg_rate = models.Avg('rate'))['avg_rate']
        profile.save()
    
    def delete(self):
        user = self.user
        super(self.__class__, self).delete()
        profile = user.profile
        profile.avg_rate = user.reviews.aggregate(avg_rate = models.Avg('rate'))['avg_rate']
        profile.save()

    def __unicode__(self):
        return self.qualification

class TutorFavorite(BaseModel):
    class Meta:
        unique_together = ('user', 'tutor')
        
    user = models.ForeignKey(User, related_name='favorite_tutors')
    tutor = models.ForeignKey(User, related_name='students_has_favorite')
    
    def __unicode__(self):
        return '%s favorite %s' % (self.user, self.tutor)


class WeekAvailability(models.Model):
    """
    A default user week availability
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

    def save(self, *args, **kwargs):
        if (self.begin > self.end and self.end.hour!=0) \
            or self.user.day_availability \
                .exclude(Q(id=self.id) | Q(end=self.begin) | Q(begin=self.end)) \
                .filter(Q(date=self.date), Q(begin__range=(self.begin, self.end)) | Q(end__range=(self.begin, self.end))):
            return
        super(self.__class__, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u'%s (%s from %s to %s)' % (self.user, self.date, self.begin, self.end)



#### STUDENT ######################################
class Child(models.Model):
    parent = models.ForeignKey(User, related_name="childs")
    child  = models.ForeignKey(User, related_name="parent_set")
    active = models.BooleanField(default=False)
    key    = models.CharField(max_length=30, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = ''.join(random.choice(string.ascii_letters + string.digits) for x in xrange(30))
        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.child


#### COMMON ########################################
class Message(BaseModel):
    user = models.ForeignKey(User, related_name='received_messages')
    to = models.ForeignKey(User, related_name='sent_messages')
    message = models.CharField(max_length=500)
    related_class = models.ForeignKey(Class, null=True, blank=True, related_name='messages')
    
    def __unicode__(self):
        return self.message
    

class NewsletterSubscription(BaseModel):
    email = models.EmailField(max_length=255, unique=True)
    email_verified = models.BooleanField(default=False)
    hash_key = models.CharField(max_length=20)

    def generate_hash_key(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in xrange(20))

    def send_verify_email(self):
        context = Context({
            'link': 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, reverse('newsletter_verify_email_address', kwargs={'key': self.hash_key}))
        })

        t = loader.get_template('profile/emails/verify_email.html')
        html = t.render(context)

        msg = EmailMessage('[Universal Tutors] Verify Email Address', html, settings.DEFAULT_FROM_EMAIL, to=[self.email])
        msg.content_subtype = "html"
        msg.send()

    def verify_email(self):
        self.email_verified = True
        self.save()

    def save(self, *args, **kwargs):
        new_subscription = False
        if not self.id:
            new_subscription = True
            self.hash_key = self.generate_hash_key()

        super(self.__class__, self).save()
        if new_subscription:
            self.send_verify_email()
