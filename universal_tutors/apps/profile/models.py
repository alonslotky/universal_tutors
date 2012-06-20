from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.template import loader, Context
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string


import re, unicodedata, random, string, datetime, os, pytz, threading, urlparse

from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged
from filebrowser.fields import FileBrowseField
from apps.common.utils.fields import AutoOneToOneField, CountryField
from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.geo import geocode_location
from apps.common.utils.model_utils import get_namedtuple_choices
from apps.common.utils.date_utils import add_minutes_to_time, first_day_of_week, minutes_difference, minutes_to_time, convert_datetime, difference_in_minutes

from apps.classes.models import Class, ClassSubject, ClassLevel, EducationalSystem
from apps.core.models import Currency
from apps.classes.settings import *

from paypal2.standart.ap import pay
from scribblar import users


class StudentManager(models.Manager):
    def get_query_set(self):
        return super(StudentManager, self).get_query_set().filter(
                    profile__type__in = [UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16],
                )

class ParentManager(models.Manager):
    def get_query_set(self):
        return super(ParentManager, self).get_query_set().filter(
                    profile__type = UserProfile.TYPES.PARENT,
                )

class TutorManager(models.Manager):
    def get_query_set(self):
        return super(TutorManager, self).get_query_set().filter(
                    profile__type = UserProfile.TYPES.TUTOR,
                )

class ActiveTutorsManager(models.Manager):
    def get_query_set(self):
        return super(ActiveTutorsManager, self).get_query_set().filter(
                    profile__type = UserProfile.TYPES.TUTOR,
                    profile__activated = True,
                )

class UnchekedCRBTutorsManager(models.Manager):
    def get_query_set(self):
        return super(EditableWorksManager, self).get_query_set().exclude(crb_checked = True).order_by('date_joined')

class Tutor(User):
    objects = ActiveTutorsManager()
    unchecked_crb = UnchekedCRBTutorsManager()

    class Meta:
        verbose_name = 'Active Tutors'
        proxy = True


class TutorList(User):
    objects = TutorManager()
    class Meta:
        verbose_name = 'Tutor'
        proxy = True

class Student(User):
    objects = StudentManager()
    class Meta:
        verbose_name = 'Student'
        proxy = True

class Parent(User):
    objects = ParentManager()
    class Meta:
        verbose_name = 'Parent'
        proxy = True


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
        (5, 'TES', 'TES'),
        (20, 'OTHER', 'Other'),
    ))

    NOTIFICATIONS_TYPES = get_namedtuple_choices('USER_NOTIFICATIONS_TYPES', (
        (0, 'BOOKED', 'A new class has been booked'),
        (1, 'CANCELED_BY_TUTOR', 'Class canceled by tutor'),
        (2, 'CANCELED_BY_STUDENT', 'Class canceled by student'),
        (3, 'INCOME', 'Credits income'),
        (4, 'ACTIVATED', 'Activated account'),
        (5, 'CLASS', 'Class is about to start'),
        (6, 'ACCEPTED_BY_TUTOR', 'A class has been accepted by tutor'),
        (7, 'REJECTED_BY_TUTOR', 'A class has been rejected by tutor'),
        (8, 'CRB_EXPIRED', 'The CRB is expired'),
        (9, 'CRB_EXPIRE_DATE', 'The CRB is going to expire in less than 60 days'),
        (10, 'MESSAGE', 'The CRB is going to expire in less than 60 days'),
    ))
    
    UPLOAD_IMAGES_PATH = 'uploads/profiles/profile_images'
    
    def get_upload_to(instance, filename):
        name, ext = os.path.splitext(filename)
        name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
        new_filename = '%s%s' % (name, ext.lower())
        return os.path.join(UserProfile.UPLOAD_IMAGES_PATH, new_filename)

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
    partners_newsletters = models.BooleanField(verbose_name=_('Partners Newsletters'))
    date_of_birth = models.DateField(verbose_name=_('Date of birth'), null=True, blank=True)
    scribblar_id = models.CharField(verbose_name=_('Scribblar ID'), max_length=100, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(verbose_name=_('Gender'), choices=GENDER_TYPES.get_choices(), default=GENDER_TYPES.MALE)
    timezone = models.CharField(verbose_name=_('Phone Timezone'), max_length=50, default=pytz.tz)
    favorite = models.ManyToManyField(User, verbose_name=_('Favorite'), related_name='favorites', null=True, blank=True)
    interests = models.ManyToManyField(ClassSubject, related_name='students', null=True, blank=True)
    
    video = models.CharField(verbose_name=_('Video'), max_length=200, null=True, blank=True)
    webcam = models.BooleanField(default=False)

    type = models.PositiveSmallIntegerField(choices=TYPES.get_choices(), default=TYPES.NONE)
    credit = models.FloatField(default=0)
    income = models.FloatField(default=0)
    currency = models.ForeignKey(Currency, null=True, blank=True)

    referral = models.PositiveSmallIntegerField(choices=REFERRAL_TYPES.get_choices(), default=TYPES.NONE)
    other_referral = models.CharField(max_length=200, null=True, blank=True)
    referral_key = models.CharField(max_length=30, null=True, blank=True)
    
    crb = models.BooleanField(default=False)
    crb_file = models.FileField(upload_to='uploads/tutor/crb_certificates', null=True, blank=True, max_length=100)
    crb_expiry_date = models.DateField(null=True, blank=True)
    crb_alert_expire_date = models.BooleanField(default = False)
    crb_alert_expired = models.BooleanField(default = False)
    
    activated = models.BooleanField(default=False)
    activation_date = models.DateTimeField(null=True, blank=True, default=None)
    featured = models.BooleanField(default=False)

    # tutor
    avg_rate = models.FloatField(default=0)
    no_reviews = models.PositiveIntegerField(default=0)
    min_credits = models.PositiveIntegerField(default=0)
    max_credits = models.PositiveIntegerField(default=0)
    
    paypal_email = models.EmailField(null=True, blank=True)
    
    classes_given = models.PositiveIntegerField(default=0)


    @property
    def crb_checked(self):
        return self.crb_expiry_date >= datetime.date.today()


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

    @property
    def total_credits(self):
        return self.credit + self.user.classes_as_student.filter(status=Class.STATUS_TYPES.BOOKED).aggregate(credits_booked = models.Sum('credit_fee'))['credits_booked']
    
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

        if self.type == self.TYPES.TUTOR:
            if self.profile_image and \
               self.profile_image != settings.DEFAULT_PROFILE_IMAGE and \
               self.about and \
               self.video:
                self.activated = True
                    
            else:
                self.activated = False
            
            if self.id:
                previous = UserProfile.objects.get(id=self.id)
                if previous.crb_expiry_date != self.crb_expiry_date:
                    self.crb_alert_expire_date = False
                    self.crb_alert_expired = False
        
        super(self.__class__, self).save(*args, **kwargs)

        user = self.user
        if self.type != self.TYPES.NONE and self.type != self.TYPES.PARENT:
            users.edit(
                userid = self.get_scribblar_id(),
                firstname = user.first_name,
                lastname = user.last_name,
                email = user.email,
                roleid = 50 if self.type == self.TYPES.TUTOR else 10,
            )

        if self.activated and not self.activation_date:
            self.activation_date = datetime.datetime.now()
            super(self.__class__, self).save(*args, **kwargs)
            self.send_notification(self.NOTIFICATIONS_TYPES.ACTIVATED, {})
                                
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

    def check_day(self, date=None, gtz=None):
        available, list = self.get_day(date, gtz=gtz)
        return available

    def get_day(self, date=None, gtz=None):
        """
        Get availability from a day
        """        
        return self.get_period(date, gtz=gtz)

    def check_week(self, date=None, begin=None, end=None, gtz=None):
        available, list = self.get_day(date, begin, end, gtz=gtz)
        return available

    def get_week(self, date=None, gtz=None):
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
                week_availability.append((day, get_day(day, gtz=gtz)))
                        
        return week_availability
        

    def check_period(self, date=None, begin=None, end=None, gtz=None):
        available, list = self.get_period(date, begin, end, gtz=gtz)
        return all([slot[1]-slot[2] > 0 for slot in list])

    def get_period(self, date=None, begin=None, end=None, gtz=None):
        """
        Get availability from a period of time
        
        Return a tuple with boolean and a list of lists: (all_slots_available, [[time, total_availability, booked], ...])
        all_slots_available - True if all slots on this period are available
        """
        user = self.user
        gtz = gtz or self.timezone
        
        date = date if date else datetime.date.today()
        user_begin = datetime.datetime.combine(date, begin if begin else datetime.time(0,0))
        user_end = datetime.datetime.combine(date, end if end else datetime.time(0,0))
        if user_end <= user_begin:
            user_end += datetime.timedelta(days=1)
        
        begin = convert_datetime(user_begin, gtz, self.timezone)
        end = convert_datetime(user_end, gtz, self.timezone)
        now = datetime.datetime.now()
        
        all_slots_available = True
        
        weekday = date.weekday()
        begin_of_week = date - datetime.timedelta(days = weekday)
        
        
        # select availability from date
        availability = user.day_availability.filter(date__in=[begin.date(), end.date()])
        if not availability:
            # select availability from a default week
            availability = user.week_availability.filter(weekday__in = [begin.weekday(), end.weekday()])
            if not availability:
                all_slots_available = False
                
        # select booking from date
        booking = user.classes_as_tutor.filter(status__in=[Class.STATUS_TYPES.BOOKED, Class.STATUS_TYPES.WAITING], date__gte=user_begin.date(), date__lt=user_end.date())

        size = 0
        availability_by_time = []
        append = availability_by_time.append
        user_time = user_begin
        user_end_period = user_begin
        time = begin
        availability_index = 0
        
        # create empty available array
        while user_time < user_end:
            end_period = time + datetime.timedelta(minutes=MINIMUM_PERIOD)
            user_end_period = user_time + datetime.timedelta(minutes=MINIMUM_PERIOD)
            append([[user_time.hour, user_time.minute, user_end_period.hour, user_end_period.minute], 0, 0])
            user_time += datetime.timedelta(minutes=MINIMUM_PERIOD)
            time = end_period
            size += 1
            if now + datetime.timedelta(minutes=20) > convert_datetime(end_period, self.timezone, pytz.utc):
                availability_index = size

        # inject total availability on array
        for period in availability:
            if hasattr(period, 'weekday'):
                begin_time = datetime.datetime.combine(begin.date(), period.begin) + datetime.timedelta(days=period.weekday-begin.weekday())
                end_time = datetime.datetime.combine(begin.date(), period.end) + datetime.timedelta(days=period.weekday-begin.weekday())

                if begin_time < begin:
                    begin_time += datetime.timedelta(days = 7)
                    end_time += datetime.timedelta(days = 7)
                if begin_time >= end:
                    begin_time -= datetime.timedelta(days = 7)
                    end_time -= datetime.timedelta(days = 7)
                if end_time <= begin_time:
                    end_time += datetime.timedelta(days=1)
                    
            else:
                begin_time = datetime.datetime.combine(period.date, period.begin)
                end_time = datetime.datetime.combine(period.date, period.end)
                            
            begin_min = difference_in_minutes(begin_time, begin) 
            end_min = difference_in_minutes(end_time, begin)

            begin_index = begin_min / MINIMUM_PERIOD
            end_index = end_min / MINIMUM_PERIOD

            # cut index outside the array
            if begin_index < 0:     begin_index = 0
            if begin_index > size:  begin_index = size
            if end_index < 0:       end_index = 0
            if end_index > size:    end_index = size
            
            for index in xrange(begin_index, end_index):
                availability_by_time[index][1] = 1 if index >= availability_index else 0 

        # inject booking on array
        for item in booking:
            # From UTC to profile timezone
            user_begin_time = convert_datetime(item.date, pytz.utc, gtz)

            begin_min = difference_in_minutes(user_begin_time, user_begin) 
            end_min = begin_min + item.duration


            begin_index = begin_min / MINIMUM_PERIOD
            end_index = end_min / MINIMUM_PERIOD

            # cut index outside the array
            if begin_index < 0:     begin_index = 0
            if begin_index > size:  begin_index = size
            if end_index < 0:       end_index = 0
            if end_index > size:    end_index = size

            for index in xrange(begin_index, end_index):
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

    def week_classes(self, date=None):
        user = self.user
        today = datetime.date.today()
        date = date if date else datetime.date.today()

        user_begin = datetime.datetime.combine(date, datetime.time(0,0)) - datetime.timedelta(days=date.weekday()) 
        user_end = user_begin + datetime.timedelta(days=7)
        
        begin = convert_datetime(user_begin, self.timezone, pytz.utc)
        end = convert_datetime(user_end, self.timezone, pytz.utc)

        booked = Class.objects.filter(Q(status__in=[Class.STATUS_TYPES.BOOKED, Class.STATUS_TYPES.DONE], date__gte=begin, date__lt=end), Q(tutor=user) | Q(student=user))
        week = [(user_begin+datetime.timedelta(days=weekday), weekday, []) for weekday in range(7)]

        for b in booked:
            date = convert_datetime(b.date, pytz.utc, self.timezone)
            week[b.date.weekday()][2].append((date, b))
            
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
        classes = list(self.get_current_classes_as_tutor())
        classes.extend(list(self.get_past_classes_as_tutor()))
        return classes
    
    def get_current_classes_as_tutor(self):
        from apps.classes.models import Class
        return self.user.classes_as_tutor.filter(status=Class.STATUS_TYPES.BOOKED)
    
    def get_past_classes_as_tutor(self):
        from apps.classes.models import Class
        return self.user.classes_as_tutor.exclude(Q(status=Class.STATUS_TYPES.BOOKED)|Q(status=Class.STATUS_TYPES.PRE_BOOKED)).order_by('-created')

    def get_classes_as_student(self):
        classes = list(self.get_current_classes_as_student())
        classes.extend(list(self.get_past_classes_as_student()))
        return classes
    
    def get_current_classes_as_student(self):
        from apps.classes.models import Class
        return self.user.classes_as_student.filter(status=Class.STATUS_TYPES.BOOKED)
    
    def get_past_classes_as_student(self):
        from apps.classes.models import Class
        return self.user.classes_as_student.exclude(Q(status=Class.STATUS_TYPES.BOOKED)|Q(status=Class.STATUS_TYPES.PRE_BOOKED)).order_by('-created')

    def get_next_class(self):
        from apps.classes.models import Class
        user = self.user
        
        now = datetime.datetime.now()
        today = now.date()
        time = now.time()
        
        try:
            return Class.objects.raw(
                    """
                    SELECT *
                    FROM classes_class
                    WHERE status = %(booked)s AND (tutor_id = %(tutor_id)s OR student_id = %(student_id)s)
                      AND date + (duration || ' minutes')::interval >= CURRENT_TIMESTAMP
                    ORDER BY date ASC
                    """ % {
                        'booked': Class.STATUS_TYPES.BOOKED,
                        'tutor_id': user.id,
                        'student_id': user.id,
                    })[0]
        except IndexError:
            return 0

    def check_crb(self):
        if self.crb_expiry_date:
            today = datetime.date.today()
            if self.crb_expiry_date < today and not self.crb_alert_expired:
                self.send_notification(self.NOTIFICATIONS_TYPES .CRB_EXPIRED, {'tutor': self.user})
                self.crb_alert_expired = True 
                self.crb_alert_expire_date = True
                super(self.__class__, self).save()
            
            if self.crb_expiry_date < today + datetime.timedelta(days=60) and not self.crb_alert_expire_date:
                self.send_notification(self.NOTIFICATIONS_TYPES.CRB_EXPIRE_DATE, {'tutor': self.user})
                self.crb_alert_expire_date = True
                super(self.__class__, self).save()


    def send_notification(self, type, context):
        subject = None
        html = None
        user = self.user

        context['user'] = user
        context['PROJECT_SITE_DOMAIN'] = settings.PROJECT_SITE_DOMAIN

        if type == self.NOTIFICATIONS_TYPES.BOOKED:
            subject = 'A new class has been booked'
            html = render_to_string('emails/booked.html', context)
        if type == self.NOTIFICATIONS_TYPES.ACCEPTED_BY_TUTOR:
            subject = 'Your class has been accepted'
            html = render_to_string('emails/accepted.html', context)
        if type == self.NOTIFICATIONS_TYPES.REJECTED_BY_TUTOR:
            subject = 'Your class has been rejected'
            html = render_to_string('emails/rejected.html', context)
        if type == self.NOTIFICATIONS_TYPES.CANCELED_BY_TUTOR:
            subject = 'Class canceled by tutor'
            html = render_to_string('emails/canceled_by_tutor.html', context)
        if type == self.NOTIFICATIONS_TYPES.CANCELED_BY_STUDENT:
            subject = 'Class canceled by student'
            html = render_to_string('emails/canceled_by_student.html', context)
        if type == self.NOTIFICATIONS_TYPES.INCOME:
            subject = 'Income credits received'
            html = render_to_string('emails/income.html', context)
        if type == self.NOTIFICATIONS_TYPES.ACTIVATED:
            subject = 'Account activated'
            html = render_to_string('emails/activated.html', context)
        if type == self.NOTIFICATIONS_TYPES.CLASS:
            subject = 'Your class is about to start'
            html = render_to_string('emails/class.html', context)
        if type == self.NOTIFICATIONS_TYPES.CRB_EXPIRED:
            subject = 'CRB expired'
            html = render_to_string('emails/crb_expired.html', context)
        if type == self.NOTIFICATIONS_TYPES.CRB_EXPIRE_DATE:
            subject = 'CRB is about to expire'
            html = render_to_string('emails/crb_expire_date.html', context)
        if type == self.NOTIFICATIONS_TYPES.MESSAGE:
            subject = 'New message'
            html = render_to_string('emails/message.html', context)
        
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
            currency = self.currency
            value = '%s %.2f' % (currency.symbol, currency.credit_value() * credits)
            self.user.movements.create(type=UserCreditMovement.MOVEMENTS_TYPES.TOPUP, credits=credits, value=value)

    def withdraw_account(self, credits):
        if self.type == self.TYPES.TUTOR:
            self.income -= credits
            super(self.__class__, self).save()
            currency = self.currency
            value = '%s %.2f' % (currency.symbol, currency.credit_value() * credits)
            self.user.movements.create(type=UserCreditMovement.MOVEMENTS_TYPES.WITHDRAW, credits=credits, value=value)


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
            no_items += 4 if user.children.count() else 0
            completeness = int(no_items / 8.0 * 100)
        else:
            completeness = 0
        
        return completeness


    def process_manual_withdraw(self):
        if self.type == self.TYPES.TUTOR:
            currency = self.currency
            credits = self.income
            credit_value = currency.credit_value()
            amount = credits * credit_value
            email = self.paypal_email
            withdraw = WithdrawItem(
                user = self.user,
                value = amount,
                credits = credits, 
                email = email,
                currency = currency,
            )
            withdraw.save()
        
            receivers = [{
                'email': email, 
                'amount': '%.2f' % amount,
                'unique_id': 'wd-%s' % withdraw.id,
            }]
        
            pay({
                'notify_url': 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, reverse('paypal-ipn')),
                'currencyCode': currency.acronym,
                'receivers': receivers,
            })

    def waiting_classes(self):
        if self.type == self.TYPES.TUTOR:
            return self.user.classes_as_tutor.filter(status=Class.STATUS_TYPES.WAITING).order_by('date')
        else:
            return self.user.classes_as_student.filter(status=Class.STATUS_TYPES.WAITING).order_by('date')           

    def booked_classes(self):
        if self.type == self.TYPES.TUTOR:
            return self.user.classes_as_tutor.filter(status=Class.STATUS_TYPES.BOOKED).order_by('date')
        else:
            return self.user.classes_as_student.filter(status=Class.STATUS_TYPES.BOOKED).order_by('date')         

    def other_classes(self):
        if self.type == self.TYPES.TUTOR:
            return self.user.classes_as_tutor.exclude(status__in=[Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.BOOKED, Class.STATUS_TYPES.WAITING]).order_by('-date')
        else:
            return self.user.classes_as_student.exclude(status__in=[Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.BOOKED, Class.STATUS_TYPES.WAITING]).order_by('-date')

    def no_messages(self):
        return Message.objects.filter(to=self.user, read = False).count()

class UserCreditMovement(BaseModel):
    class Meta:
        ordering = ('-created',)
    
    MOVEMENTS_TYPES = get_namedtuple_choices('USER_MOVEMENTS_TYPES', (
        (0, 'PAYMENT', 'Payment for a class'),
        (1, 'INCOME', 'Class income'),
        (2, 'CANCELED_BY_TUTOR', 'Class canceled by tutor (Refund)'),
        (3, 'CANCELED_BY_STUDENT', 'Class canceled by student (Refund)'),
        (4, 'STOPPED_BY_STUDENT', 'Stopped by student (Refund)'),
        (5, 'TOPUP', 'Top-up account'),
        (6, 'WITHDRAW', 'Withdraw to PayPal Account'),
        (7, 'REJECTED_BY_TUTOR', 'Rejected by tutor (Refund)'),
    ))

    user = models.ForeignKey(User, related_name='movements')
    type = models.PositiveSmallIntegerField(choices = MOVEMENTS_TYPES.get_choices())
    credits = models.FloatField()
    value = models.CharField(max_length=15, null=True, blank=True)
    related_class = models.ForeignKey(Class, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.get_type_display(), self.credits)

class TopUpItem(BaseModel):
    """
    A TopUpItem
    """
    class Meta:
        ordering = ['-created']

    STATUS_TYPES = get_namedtuple_choices('TOPUP_STATUS_TYPES', (
        (0, 'CART', 'On Cart'),
        (1, 'CANCELED', 'Canceled'),
        (2, 'FLAGGED', 'Flagged'),
        (3, 'HACKED', 'HACKED! The amount paid were changed'),
        (99, 'DONE', 'Done'),
    ))
    
    user = models.ForeignKey(User, related_name = 'topups')
    currency = models.ForeignKey(Currency, related_name='topups')
    value = models.FloatField()
    credits = models.PositiveIntegerField()
    status = models.PositiveSmallIntegerField(choices = STATUS_TYPES.get_choices(), default = STATUS_TYPES.CART)
    invoice = models.CharField(max_length = 20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice:
            while True:
                self.invoice = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(20))
                if not TopUpItem.objects.filter(invoice=self.invoice).exclude(id=self.id):
                    break
        super(self.__class__, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "[%s] %s: %s" % (self.user, self.get_status_display(), self.credits)

    def topup(self):
        if self.status != self.STATUS_TYPES.DONE and self.status != self.STATUS_TYPES.FLAGGED:
            self.status = self.STATUS_TYPES.DONE
            super(self.__class__, self).save()
            self.user.profile.topup_account(self.credits)
        elif self.status == self.STATUS_TYPES.FLAGGED:
            self.status = self.STATUS_TYPES.DONE
            super(self.__class__, self).save()
            
    def flagged(self):
        if self.status != self.STATUS_TYPES.DONE and self.status != self.STATUS_TYPES.FLAGGED:
            self.status = self.STATUS_TYPES.FLAGGED
            super(self.__class__, self).save()
            self.user.profile.topup_account(self.credits)

    def cancel(self):
        if self.status != self.STATUS_TYPES.DONE and self.status != self.STATUS_TYPES.FLAGGED:
            self.status = self.STATUS_TYPES.CANCELED
            self.save()

    def set_as_hacked(self):
        if self.status != self.STATUS_TYPES.DONE and self.status != self.STATUS_TYPES.FLAGGED:
            self.status = self.STATUS_TYPES.HACKED
            self.save()


class WithdrawItem(BaseModel):
    """
    A Withdraw item
    """
    class Meta:
        ordering = ['-created']

    STATUS_TYPES = get_namedtuple_choices('WITHDRAW_STATUS_TYPES', (
        (0, 'PROCESSING', 'Processing'),
        (1, 'CANCELED', 'Canceled'),
        (2, 'PENDING', 'Pending'),
        (3, 'HACKED', 'HACKED! The amount received were changed'),
        (99, 'DONE', 'Done'),
    ))
    
    user = models.ForeignKey(User, related_name = 'withdraws')
    currency = models.ForeignKey(Currency, related_name='withdraws')
    value = models.FloatField()
    credits = models.PositiveIntegerField()
    status = models.PositiveSmallIntegerField(choices = STATUS_TYPES.get_choices(), default = STATUS_TYPES.PROCESSING)
    invoice = models.CharField(max_length = 20, null=True, blank=True)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        if not self.invoice:
            while True:
                self.invoice = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(20))
                if not TopUpItem.objects.filter(invoice=self.invoice).exclude(id=self.id):
                    break
        super(self.__class__, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "[%s] %s: %s" % (self.user, self.get_status_display(), self.credits)

    def complete(self):
        if self.status != self.STATUS_TYPES.DONE and self.status != self.STATUS_TYPES.PENDING:
            self.status = self.STATUS_TYPES.DONE
            super(self.__class__, self).save()
            self.user.profile.withdraw_account(self.credits)
        elif self.status == self.STATUS_TYPES.PENDING:
            self.status = self.STATUS_TYPES.DONE
            super(self.__class__, self).save()
    
    def pending(self):
        if self.status != self.STATUS_TYPES.DONE and self.status != self.STATUS_TYPES.PENDING:
            self.status = self.STATUS_TYPES.PENDING
            super(self.__class__, self).save()
            self.user.profile.withdraw_account(self.credits)

    def cancel(self):
        if self.status != self.STATUS_TYPES.DONE and self.status != self.STATUS_TYPES.PENDING:
            self.status = self.STATUS_TYPES.CANCELED
            self.save()

    def set_as_hacked(self):
        if self.status != self.STATUS_TYPES.DONE and self.status != self.STATUS_TYPES.PENDING:
            self.status = self.STATUS_TYPES.HACKED
            self.save()


### TUTOR ###########
class TutorSubject(models.Model):
    user = models.ForeignKey(User, related_name='subjects')
    system = models.ForeignKey(EducationalSystem, related_name='tutors')
    subject = models.ForeignKey(ClassSubject, related_name='tutors')
    level = models.ForeignKey(ClassLevel, related_name='tutors')
    credits = models.FloatField()
    
    def save(self, *args, **kwargs):
        if not TutorSubject.objects.filter(user=self.user, system=self.system, subject=self.subject, level=self.level).exclude(id=self.id):
            super(self.__class__, self).save(*args, **kwargs)
            user = self.user
            profile = user.profile 
            results = user.subjects.aggregate(min_credits = models.Min('credits'), max_credits = models.Max('credits'))   
            profile.min_credits = results['min_credits']
            profile.max_credits = results['max_credits']
            profile.save()
    
    def __unicode__(self):
        return '%s (%s)' % (self.subject, self.level)


class TutorQualification(models.Model):
    def get_upload_to(instance, filename):
        name, ext = os.path.splitext(filename)
        name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
        new_filename = '%s%s' % (name, ext.lower())
        return os.path.join('uploads/profiles/qualifications/documents', new_filename)

    user = models.ForeignKey(User, related_name='qualifications')
    qualification = models.CharField(max_length=200)
    document = models.FileField(null=True, blank=True, upload_to=get_upload_to)

    def save(self, *args, **kwargs):
        if not TutorQualification.objects.filter(user=self.user, qualification__iexact=self.qualification).exclude(id=self.id):
            super(self.__class__, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.qualification
    

class TutorReview(BaseModel):
    user = models.ForeignKey(User, related_name='reviews_as_tutor')
    rate = models.PositiveSmallIntegerField(default = 0)
    related_class = models.ForeignKey(Class, related_name='tutor_reviews')
    is_active= models.BooleanField(default=True)
    text = models.TextField()
    
    def save(self, *args, **kwargs):
        user = self.user
        sanctioned = False
        if not self.id and self.rate <= 1:
            self.is_active = False
            
            sanctioned = True
            
        super(TutorReview, self).save(*args, **kwargs)

        if sanctioned:            
            html = render_to_string('emails/bad_review_tutor.html', {
                'link': 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, '/admin/profile/badreview/%s/'% self.id ),
                'PROJECT_SITE_DOMAIN': settings.PROJECT_SITE_DOMAIN,
            })
            
            subject = 'Bad Tutor Review'
            sender = 'Universal Tutors <%s>' % settings.DEFAULT_FROM_EMAIL
            to = [settings.CONTACT_EMAIL]
                    
            email_message = EmailMessage(subject, html, sender, to)
            email_message.content_subtype = 'html'
            
            t = threading.Thread(target=email_message.send, kwargs={'fail_silently': True})
            t.setDaemon(True)
            t.start()

        profile = user.profile
        profile.avg_rate = user.reviews_as_tutor.filter(is_active=True).aggregate(avg_rate = models.Avg('rate'))['avg_rate']
        profile.no_reviews = user.reviews_as_tutor.filter(is_active=True).count()
        profile.save()
    
    def delete(self):
        user = self.user
        super(self.__class__, self).delete()
        profile = user.profile
        reviews = user.reviews_as_tutor.aggregate(avg_rate = models.Avg('rate'), no_reviews = models.Count('rate'))
        profile.avg_rate = reviews['avg_rate']
        profile.no_reviews = reviews['no_reviews']
        profile.save()

    def __unicode__(self):
        return '%s (%s)' % (self.text, self.rate)
    
    
class TutorInactiveReviewsManager(models.Manager):
    def get_query_set(self):
        return super(TutorInactiveReviewsManager, self).get_query_set().filter(is_active=False)

class BadReview(TutorReview):
    objects = TutorInactiveReviewsManager()

    class Meta:
        verbose_name = 'Bad Review'
        proxy = True
        


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
    email_sent = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.message

    def send_email(self):
        if not self.read and not self.email_sent:
            user = self.to
            profile = user.profile
            profile.send_notification(profile.NOTIFICATIONS_TYPES.MESSAGE, {'message': self})
            self.email_sent = True
            super(self.__class__, self).save()


class Report(BaseModel):
    class Meta:
        ordering = ('created',)
    
    violator = models.ForeignKey(User, related_name='received_report')
    user = models.ForeignKey(User, related_name='sent_report')
    description = models.TextField()
    
    def send_report(self):
        if self.violator.profile.type in [UserProfile.TYPES.STUDENT, UserProfile.TYPES.TUTOR]:
            subject = 'A new report about a %s was added' % self.violator.profile.get_type_display()
            if self.violator.profile.type == UserProfile.TYPES.STUDENT:
                admin_url = reverse('admin:profile_reportedstudent_change', args=(self.id,))
            else:
                admin_url = reverse('admin:profile_reportedtutor_change', args=(self.id,))
            html = render_to_string('emails/user_report.html', {
                'violator': self.violator,
                'user': self.user,
                'description': self.description,
                'report_url': 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, admin_url)
                
            })
    
            if subject and html:
                sender = 'Universal Tutors <%s>' % settings.DEFAULT_FROM_EMAIL
                to = [settings.CONTACT_EMAIL]
                        
                email_message = EmailMessage(subject, html, sender, to)
                email_message.content_subtype = 'html'
                
                t = threading.Thread(target=email_message.send, kwargs={'fail_silently': True})
                t.setDaemon(True)
                t.start()
        
    
    def save(self, *args, **kwargs):
        super(self.__class__, self).save()
        self.send_report()
    
    def __unicode__(self):
        return '%s reported %s' % (self.user, self.violator)

class ReportedTutorManager(models.Manager):
    def get_query_set(self):
        return super(ReportedTutorManager, self).get_query_set().filter(violator__profile__type = UserProfile.TYPES.TUTOR)

class ReportedStudentManager(models.Manager):
    def get_query_set(self):
        return super(ReportedStudentManager, self).get_query_set().filter(violator__profile__type__in = [UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16])

class ReportedStudent(Report):
    objects = ReportedStudentManager()

    class Meta:
        verbose_name = 'Reported Student'
        proxy = True

class ReportedTutor(Report):
    objects = ReportedTutorManager()

    class Meta:
        verbose_name = 'Reported Tutor'
        proxy = True

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
            'PROJECT_SITE_DOMAIN': settings.PROJECT_SITE_DOMAIN,
        })

        if subject and html:            
            sender = 'Universal Tutors <%s>' % settings.DEFAULT_FROM_EMAIL
            to = ['%s <%s>' % (self.name, self.email)]
                    
            email_message = EmailMessage(subject, html, sender, to)
            email_message.content_subtype = 'html'
            
            t = threading.Thread(target=email_message.send, kwargs={'fail_silently': True})
            t.setDaemon(True)
            t.start()


#### TOPUP CREDITS #######################################################
def topup_successful(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.txn_type.lower() == 'web_accept':         
        try:
            topup = TopUpItem.objects.get(id = ipn_obj.item_number)
            if topup.value == float(ipn_obj.mc_gross):
                topup.topup()
            else:
                topup.set_as_hacked()
                paypal_error(type='topup_hacked')
        except TopUpItem.DoesNotExist:
            paypal_error()

    elif ipn_obj.txn_type.lower() == 'masspay':
        withdraw_complete(sender, **kwargs)
    
def topup_flagged(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.txn_type.lower() == 'web_accept':         
        try:
            topup = TopUpItem.objects.get(id = ipn_obj.item_number)
            if topup.value == float(ipn_obj.mc_gross):
                topup.flagged()
            else:
                topup.set_as_hacked()
                paypal_error(type='topup_hacked')
        except TopUpItem.DoesNotExist:
            paypal_error()
            
    elif ipn_obj.txn_type.lower() == 'masspay':
        withdraw_complete(sender, **kwargs)


def withdraw_complete(sender, **kwargs):
    ipnobj = sender
    query = urlparse.parse_qs(ipnobj.query)

    i = 1
    while True:
        gross = query.get('mc_gross_%s' % i, [''])[0]
        status = query.get('status_%s' % i, [''])[0].lower()
        variable, unique_id = query.get('unique_id_%s' % i, ['wd-0'])[0].split('-')
        email = query.get('receiver_email_%s' % i, [''])[0]
        if not gross and not status:
            break
        
        try:
            withdraw = WithdrawItem.objects.get(id = unique_id)
            if withdraw.value == float(gross):
                if status=='completed' or status=='pending':
                    if status == 'completed':
                        withdraw.complete()
                    else:
                        withdraw.pending()
                else:
                    withdraw.error()
                    paypal_error(type='withdraw_error', email=email)
            else:
                withdraw.set_as_hacked()
                paypal_error(type='withdraw_hacked', email=email)
                             
        except WithdrawItem.DoesNotExist:
            paypal_error(type='withdraw_invalid', email=email)

        i += 1


def paypal_error(type='topup_invalid', email=None):
    if type=='topup_hacked':
        subject = 'Hacked PayPal IPN'
        html = 'An hacked PayPal IPN topup has been received. Please check if is only a system error first.'
    elif type=='topup_invalid':
        subject = 'Invalid PayPal IPN'
        html = 'An invalid PayPal IPN topup has been received.'
    elif type=='withdraw_hacked':
        subject = 'Hacked PayPal IPN'
        html = 'An hacked PayPal IPN withdraw has been received from <%s>. Please check if is only a system error first.' % email
    elif type=='withdraw_invalid':
        subject = 'Invalid PayPal IPN'
        html = 'An invalid PayPal IPN topup has been received from <%s>.' % email
    elif type=='withdraw_error':
        subject = 'Withdraw PayPal Error'
        html = 'An error occurred during a payment (withdraw) from email <%s>. Please check if email is from a valid PayPal account.' % email
    
    sender = 'Universal Tutors <%s>' % settings.DEFAULT_FROM_EMAIL
    to = [settings.CONTACT_EMAIL]
            
    email_message = EmailMessage(subject, html, sender, to)
    email_message.content_subtype = 'html'
    
    t = threading.Thread(target=email_message.send, kwargs={'fail_silently': True})
    t.setDaemon(True)
    t.start()


payment_was_successful.connect(topup_successful, dispatch_uid='topup_successful')
payment_was_flagged.connect(topup_flagged, dispatch_uid='topup_flagged')

