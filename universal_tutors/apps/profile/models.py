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
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string


import re, unicodedata, random, string, datetime, os, pytz, threading, urlparse

from filebrowser.fields import FileBrowseField
from apps.common.utils.fields import AutoOneToOneField, CountryField
from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.geo import geocode_location
from apps.common.utils.model_utils import get_namedtuple_choices
from apps.common.utils.date_utils import add_minutes_to_time, first_day_of_week, minutes_difference, minutes_to_time

from apps.classes.models import Class, ClassSubject
from apps.core.models import Currency
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
        (0, 'SEARCH', 'Search engines'),
        (1, 'FACEBOOK', 'Facebook'),
        (2, 'TWITTER', 'Twitter'),
        (3, 'GOOGLE', 'Google+'),
        (4, 'FRIEND', 'A friend'),
        (20, 'OTHER', 'Other'),
    ))

    NOTIFICATIONS_TYPES = get_namedtuple_choices('USER_NOTIFICATIONS_TYPES', (
        (0, 'BOOKED', 'A new class has been booked'),
        (1, 'CANCELED_BY_TUTOR', 'Class canceled by tutor'),
        (2, 'CANCELED_BY_STUDENT', 'Class canceled by student'),
        (3, 'INCOME', 'Credits income'),
    ))
    
    def get_upload_to(instance, filename):
        name, ext = os.path.splitext(filename)
        name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
        new_filename = '%s%s' % (name, ext.lower())
        return os.path.join('uploads/profiles/profile_images', new_filename)

    user = AutoOneToOneField(User, related_name="profile")
    
    about = models.CharField(verbose_name=_('Description'), max_length=500, null=True, blank=True)
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
    favorite = models.ManyToManyField(User, verbose_name=_('Favorite'), related_name='favorites', null=True, blank=True)
    interests = models.ManyToManyField(ClassSubject, related_name='students')
    
    video = models.CharField(verbose_name=_('Video'), max_length=200, null=True, blank=True)

    type = models.PositiveSmallIntegerField(choices=TYPES.get_choices(), default=TYPES.NONE)
    credit = models.FloatField(default=0)
    income = models.FloatField(default=0)

    referral = models.PositiveSmallIntegerField(choices=REFERRAL_TYPES.get_choices(), default=TYPES.NONE)
    other_referral = models.CharField(max_length=200, null=True, blank=True)
    referral_key = models.CharField(max_length=30, null=True, blank=True)
    
    crb = models.BooleanField(default=False)
    crb_file = models.FileField(upload_to='uploads/tutor/crb_certificates', null=True, blank=True, max_length=100)

    # tutor
    avg_rate = models.FloatField(default=0)
    no_reviews = models.PositiveIntegerField(default=0)
    min_credits = models.PositiveIntegerField(default=0)
    max_credits = models.PositiveIntegerField(default=0)
    
    classes_given = models.PositiveIntegerField(default=0)

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
        today = datetime.date.today()        
        # there are no problem because 29 Feb less 16 years it's 29 Feb too
        date = datetime.date(today.year - 16, today.month, today.day)

        if self.date_of_birth and self.date_of_birth <= date:
            return self
        
        try:
            return self.user.parent_set.filter(active=True).latest('id').parent
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

    def delete(self):
        try:
            users.delete(user_id=self.scribblar_id)
        except:
            pass
        
        super(self.__class__, self).delete()

    def get_video_id(self):
        video_id = None
        if self.video:
            try:
                parsed = urlparse.urlparse(self.video)
                video_id = urlparse.parse_qs(parsed.query)['v'][0]
            except IndexError:
                if self.video.find('http://youtu.be/') > 0:
                    video_id = self.video.replace('http://youtu.be/', '')
            except KeyError:
                if self.video.find('http://youtu.be/') > 0:
                    video_id = self.video.replace('http://youtu.be/', '')
        return video_id 


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
        today = datetime.date.today()
        date = date if date else datetime.date.today()
        date = date - datetime.timedelta(days=date.weekday())
        
        get_day = self.get_day
        
        week_availability = []
        for dt in xrange(0,7):
            day = date + datetime.timedelta(days=dt)
            
            if day < today:
                week_availability.append((day, (False, [])))
            else:
                week_availability.append((day, get_day(day)))
                        
        return week_availability
        

    def check_period(self, date=None, begin=None, end=None):
        available, list = self.get_period(date, begin, end)
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
        booking = user.classes_as_tutor.filter(status=Class.STATUS_TYPES.BOOKED, date=date)

        size = 0
        availability_by_time = []
        append = availability_by_time.append
        time = datetime.time(begin.hour, begin.minute)
        
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
            
            for index in xrange(start_index, end_index):
                availability_by_time[index][1] = 0 if hasattr(period, 'day_off') and period.dayoff else 1
                

        # inject booking on array
        for item in booking:
            start_index = (item.start.hour - begin.hour) * PERIOD_STEPS + (item.start.minute / MINIMUM_PERIOD)
            if item.end.hour != 0:
                end_index = (item.end.hour - begin.hour) * PERIOD_STEPS + (item.end.minute / MINIMUM_PERIOD)
            else:
                end_index = size
            
            # cut index outside the array
            if start_index < 0:     start_index = 0
            if start_index > size:  start_index = size
            if end_index < 0:       end_index = 0
            if end_index > size:    end_index = size

            for index in xrange(start_index, end_index):
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
            username = user.username
            try:
                scribblar_user = users.add(
                    username = user.username,
                    firstname = user.first_name,
                    lastname = user.last_name,
                    email = user.email,
                    roleid = 50 if self.type == self.TYPES.TUTOR else 10,
                )
            except:
                scribblar_user = None
                for s_user in users.list():
                    if s_user['username'] == username:
                        scribblar_user = s_user
                        break
                
            if scribblar_user:
                self.scribblar_id = scribblar_user['userid']
                super(self.__class__, self).save()
        
        return self.scribblar_id


    def get_classes_as_tutor(self):
        from apps.classes.models import Class
        return self.user.classes_as_tutor.exclude(status=Class.STATUS_TYPES.PRE_BOOKED)

    def get_classes_as_student(self):
        from apps.classes.models import Class
        return self.user.classes_as_student.exclude(status=Class.STATUS_TYPES.PRE_BOOKED)

    def get_next_class(self):
        from apps.classes.models import Class
        user = self.user
        
        now = datetime.datetime.now()
        today = now.date()
        time = now.time()
        
        try:
            return Class.objects.filter(Q(status=Class.STATUS_TYPES.BOOKED), Q(tutor=user) | Q(student=user)).filter(Q(date__gt=today) | Q(date=today, end__gte=time))[0]
        except IndexError:
            return 0

    def send_notification(self, type, context):
        subject = None
        html = None
        user = self.user

        context['user'] = user
        context['PROJECT_SITE_DOMAIN'] = settings.PROJECT_SITE_DOMAIN

        if type == self.NOTIFICATIONS_TYPES.BOOKED:
            subject = 'A new class has been booked'
            html = render_to_string('emails/booked.html', context)
        if type == self.NOTIFICATIONS_TYPES.CANCELED_BY_TUTOR:
            subject = 'Class canceled by tutor'
            html = render_to_string('emails/canceled_by_tutor.html', context)
        if type == self.NOTIFICATIONS_TYPES.CANCELED_BY_STUDENT:
            subject = 'Class canceled by student'
            html = render_to_string('emails/canceled_by_student.html', context)
        if type == self.NOTIFICATIONS_TYPES.INCOME:
            subject = 'Income credits received'
            html = render_to_string('emails/income.html', context)
        
        if subject and html:            
            sender = 'Universal Tutors <%s>' % settings.DEFAULT_FROM_EMAIL
            to = ['%s <%s>' % (user.get_full_name(), user.email)]
                    
            email_message = EmailMessage(subject, html, sender, to)
            email_message.content_subtype = 'html'
            
            t = threading.Thread(target=email_message.send, kwargs={'fail_silently': True})
            t.setDaemon(True)
            t.start()
    
    def topup_account(self, credits):
        if self.type == self.TYPES.STUDENT or self.type == self.TYPES.UNDER16:
            self.credit += credits
            super(self.__class__, self).save()
            self.user.movements.create(type=UserCreditMovement.MOVEMENTS_TYPES.TOPUP, credits=credits)


    def get_completeness(self):
        user = self.user
        no_items = 4.0
        if self.type == self.TYPES.TUTOR:
            no_items += 1 if self.video else 0
            no_items += 1 if self.crb else 0
            no_items += 1 if user.subjects.count() else 0
            no_items += 1 if user.qualifications.count() else 0
            no_items += 1 if user.week_availability else 0
            no_items += 1 if self.profile_image and self.profile_image != settings.DEFAULT_PROFILE_IMAGE else 0
            
            completeness = int(no_items / 10.0 * 100)

        elif self.type == self.TYPES.STUDENT or self.type == self.TYPES.UNDER16:
            no_items += 1 if self.interests.count() else 0
            no_items += 1 if self.profile_image and self.profile_image != settings.DEFAULT_PROFILE_IMAGE else 0
        
            completeness = int(no_items / 6.0 * 100)
        elif self.type == self.TYPES.PARENT:
            no_items += 4 if self.children.count() else 0
            completeness = int(no_items / 8.0 * 100)
        else:
            completeness = 0
        
        return completeness
            

class UserCreditMovement(BaseModel):
    class Meta:
        ordering = ('-created',)
    
    MOVEMENTS_TYPES = get_namedtuple_choices('USER_MOVEMENTS_TYPES', (
        (0, 'PAYMENT', 'Payment for a class'),
        (1, 'INCOME', 'Class income'),
        (2, 'CANCELED_BY_TUTOR', 'Class canceled by tutor (Refund)'),
        (3, 'CANCELED_BY_STUDENT', 'Class canceled by student (Income)'),
        (4, 'STOPPED_BY_STUDENT', 'Stopped by student (Refund)'),
        (5, 'TOPUP', 'Top-up account'),
    ))

    user = models.ForeignKey(User, related_name='movements')
    type = models.PositiveSmallIntegerField(choices = MOVEMENTS_TYPES.get_choices())
    credits = models.FloatField()

    def __unicode__(self):
        return '%s: %s' % (self.get_type_display(), self.credits)


### TUTOR ###########
class TutorSubject(models.Model):
    user = models.ForeignKey(User, related_name='subjects')
    subject = models.ForeignKey(ClassSubject, related_name='tutors')
    credits = models.FloatField()
    
    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        user = self.user
        profile = user.profile 
        results = user.subjects.aggregate(min_credits = models.Min('credits'), max_credits = models.Max('credits'))   
        profile.min_credits = results['min_credits']
        profile.max_credits = results['max_credits']
        profile.save()
    
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
    user = models.ForeignKey(User, related_name='reviews_as_tutor')
    rate = models.PositiveSmallIntegerField(default = 0)
    related_class = models.ForeignKey(Class, related_name='tutor_reviews')
    text = models.TextField()
    
    def save(self, *args, **kwargs):
        user = self.user
        super(self.__class__, self).save(*args, **kwargs)
        profile = user.profile
        profile.avg_rate = user.reviews_as_tutor.aggregate(avg_rate = models.Avg('rate'))
        profile.no_rate = user.reviews_as_tutor.count()
        profile.save()
    
    def delete(self):
        user = self.user
        super(self.__class__, self).delete()
        profile = user.profile
        reviews = user.reviews_as_tutor.aggregate(avg_rate = models.Avg('rate'), no_reviews = models.Count('rate'))
        profile.avg_rate = reviews['avg_rate']
        profile.no_rate = reviews['no_reviews']
        profile.save()

    def __unicode__(self):
        return '%s (%s)' % (self.text, self.rate)

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
    day_off = models.BooleanField(default=False)

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
    parent = models.ForeignKey(User, related_name="children")
    child  = models.ForeignKey(User, related_name="parent_set")
    active = models.BooleanField(default=False)
    key    = models.CharField(max_length=30, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = ''.join(random.choice(string.ascii_letters + string.digits) for x in xrange(30))
        super(self.__class__, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.child


class StudentReview(BaseModel):
    user = models.ForeignKey(User, related_name='reviews_as_student')
    related_class = models.ForeignKey(Class, related_name='student_reviews')
    text = models.TextField()

    def __unicode__(self):
        return self.text



#### COMMON ########################################
class Message(BaseModel):
    class Meta:
        ordering = ('created',)
    
    user = models.ForeignKey(User, related_name='sent_messages')
    to = models.ForeignKey(User, related_name='received_messages')
    message = models.CharField(max_length=500)
    related_class = models.ForeignKey(Class, null=True, blank=True, related_name='messages')
    read = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.message


class Report(BaseModel):
    class Meta:
        ordering = ('created',)
    
    violator = models.ForeignKey(User, related_name='received_report')
    user = models.ForeignKey(User, related_name='sent_report')
    description = models.TextField()
    
    def __unicode__(self):
        return '%s reported %s' (self.user, self.violator)


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


class Referral(BaseModel):
    user = models.ForeignKey(User, related_name='referrals')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    key = models.CharField(max_length=30, unique=True, db_index=True)
    used = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        is_new = not self.id
        if is_new:
            safe = False
            while True:
                self.key = ''.join(random.choice(string.ascii_letters + string.digits) for x in xrange(30))
                if not Referral.objects.filter(key = self.key):
                    break
        
        super(self.__class__, self).save(*args, **kwargs)
        if is_new:
            self.send_notification()

    def send_notification(self):
        subject = '%s referral Universal Tutors to you' % self.user.get_full_name()
        html = render_to_string('emails/referral.html', {
            'sender': self.user,
            'name': self.name,
            'key': self.key,
        })

        if subject and html:            
            sender = 'Universal Tutors <%s>' % settings.DEFAULT_FROM_EMAIL
            to = ['%s <%s>' % (self.name, self.email)]
                    
            email_message = EmailMessage(subject, html, sender, to)
            email_message.content_subtype = 'html'
            
            t = threading.Thread(target=email_message.send, kwargs={'fail_silently': True})
            t.setDaemon(True)
            t.start()

