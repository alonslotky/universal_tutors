from django import http
from django.conf import settings
from django.http import  HttpResponseServerError
from django.db.models import Q, Sum, Max
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.common.utils.view_utils import main_render
from apps.profile.models import *
from apps.classes.models import *
from apps.core.models import Video, Currency
from apps.core.utils import *

from ordereddict import OrderedDict
import datetime, random


@main_render(template='core/home.html')
def home(request):
    user = request.user

    featured_tutors = Tutor.objects.select_related().filter(profile__featured=True).order_by('-profile__activation_date')
    no_featured_tutors = featured_tutors.count()

    try:
        video = Video.objects.filter(type=Video.VIDEO_TYPES.HOME, active=True).latest('id')
    except Video.DoesNotExist:
        video = None

    return {
        'featured_tutors': random.sample(featured_tutors, 3) if no_featured_tutors > 3 else random.sample(featured_tutors, no_featured_tutors),
        'video': video,
    }

        

@main_render(template='core/search.html')
def search(request):
    user = request.user
    tutors = None
    
    subjects = set()
    levels = set()
    
    query = request.GET.get('text', '')
    what = request.GET.get('what', None)
    
    system = request.GET.get('system', '')
    subject = request.GET.get('subject', '')
    level = request.GET.get('level', '')

    try:
        price_from = int(request.GET.get('price-from', 0))
    except ValueError:
        price_from = 0
        
    try:
        price_to = int(request.GET.get('price-to', 0))
    except ValueError:
        price_to = 0
    
    day = int(request.GET.get('day', -1))
    time = int(request.GET.get('time', -1))
    crb = request.GET.get('crb', False)
    sort = request.GET.get('sort', 'price')
    favorite = request.GET.get('favorite', False)
    
    results_per_page = request.GET.get('results_per_page', 10)
    
    tutors = Tutor.objects.select_related()    
    
    today = datetime.date.today()
    
    if crb:
        tutors = tutors.filter(profile__crb_expiry_date__gte=today)
    
    if query:
        if what == 'tutor':
            words = query.split()
            for word in words:
                tutors = tutors.filter(Q(first_name__icontains=word) | Q(last_name__icontains=word) | Q(username__icontains=word))
        elif what == 'subject':
            words = query.split()
            for word in words:
                tutors = tutors.filter(Q(subjects__subject__subject__icontains=word) | Q(subjects__level__level__icontains=word))

    if system:
        tutors = tutors.filter(subjects__system__id = system)

    if subject:
        tutors = tutors.filter(subjects__subject__id = subject)

    if level:
        tutors = tutors.filter(subjects__level__id = level)

    if favorite and user.is_authenticated():
        tutors = tutors.filter(profile__favorite = user)
    
    if price_from:
        tutors = tutors.filter(Q(subjects__credits__gte=price_from))

    if price_to:
        tutors = tutors.filter(Q(subjects__credits__lte=price_to))
    
    if day >= 0 and time >=0:
        tutors = tutors.filter(week_availability__weekday=day, week_availability__begin__lte=datetime.time(time,0), week_availability__end__gte=datetime.time(time,0))
    else:
        if day >= 0:
            tutors = tutors.filter(week_availability__weekday=day)    
        if time >= 0:
            tutors = tutors.filter(week_availability__begin=datetime.time(time,0))

    if sort == 'price':
        tutors = tutors.annotate(price = Max('subjects__credits')).order_by('price')
    elif sort == 'rating':
        tutors = tutors.distinct().order_by('-profile__avg_rate')
    elif sort == 'classes':
        tutors = tutors.distinct().order_by('-profile__classes_given')
    
    if system:
        try:
            selected_system = EducationalSystem.objects.get(id = system)
        except EducationalSystem.DoesNotExist:
            selected_system = None
    else:
        selected_system = None
          
    return { 
        'systems': EducationalSystem.objects.all(),
        'subjects': ClassSubject.objects.all(),
        'levels': ClassLevel.objects.all(),
        'selected_system': selected_system,
        'results_per_page': results_per_page,
        'user': user,
        'tutors': tutors.distinct(),
        'currencies': Currency.objects.all(),
    }


@main_render(template='core/reports/base.html')
def reports(request):
    user = request.user

    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()
    
    return {}


@main_render(template='core/reports/students.html')
def reports_students(request):
    user = request.user

    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()
    
    today = datetime.datetime.today()
    
    year = int(request.GET.get('year', 0) or 0)
    month = int(request.GET.get('month', 0) or 0)
    day = int(request.GET.get('day', 0) or 0)
    
    if year and month and day:
        students_signed_up = User.objects.filter(profile__type__in = [UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16]) \
                        .filter(date_joined__year = year, date_joined__month = month, date_joined__day = day).count()
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year, date__month = month, date__day = day)
        
    elif year and month:
        students_signed_up = User.objects.filter(profile__type__in = [UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16]) \
                        .filter(date_joined__year = year, date_joined__month = month).count()
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year, date__month = month)
    
    elif year:
        students_signed_up = User.objects.filter(profile__type__in = [UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16]) \
                        .filter(date_joined__year = year).count()
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year)
    
    else:
        students_signed_up = User.objects.filter(profile__type__in = [UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16]).count()
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING])
    
    
    price_per_hour = init_price_per_hour()
    total_price = init_total_price()
    class_time = init_class_time()
    
    system = OrderedDict()
    subject = OrderedDict()
    level = OrderedDict()
    subject_level = OrderedDict()
    users = set()
    
    for class_ in classes:
        add_student_to_dict(class_time, '%s minutes' % class_.duration, class_)
        if class_.system: add_student_to_dict(system, '%s' % class_.system, class_)
        if class_.level: add_student_to_dict(level, '%s' % class_.level, class_)
        if class_.only_subject: add_student_to_dict(subject, '%s' % class_.only_subject, class_)
        add_student_to_dict(subject_level, '%s' % class_.subject, class_)
        add_student_to_dict(price_per_hour, get_price_per_hour_slot(class_), class_)
        add_student_to_dict(total_price, get_total_price_slot(class_), class_)
        users.add(class_.student.username)
    
    return {
        'price_per_hour': price_per_hour,
        'total_price': total_price,
        'class_time': class_time,
        'system': system,
        'level': level,
        'subject': subject,
        'subject_level': subject_level,
        'total_students': User.objects.filter(profile__type__in = [UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16]).count(),
        'students_taking_classes': len(users),
        'students_signed_up': students_signed_up,
        'years': [(y,y) for y in reversed(range(2012, today.year + 1))],
        'months': [(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),
                  (7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December'),],
        'days': [(d,d) for d in range(1, 32)],
        'day': day,
        'month': month,
        'year': year,
    }


@main_render(template='core/reports/tutors.html')
def reports_tutors(request):
    user = request.user

    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()
    
    today = datetime.datetime.today()
    
    year = int(request.GET.get('year', 0) or 0)
    month = int(request.GET.get('month', 0) or 0)
    day = int(request.GET.get('day', 0) or 0)
    
    if year and month and day:
        tutors_signed_up = User.objects.filter(profile = UserProfile.TYPES.TUTOR) \
                        .filter(date_joined__year = year, date_joined__month = month, date_joined__day = day).count()
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year, date__month = month, date__day = day)
        
    elif year and month:
        tutors_signed_up = User.objects.filter(profile = UserProfile.TYPES.TUTOR) \
                        .filter(date_joined__year = year, date_joined__month = month).count()
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year, date__month = month)
    
    elif year:
        tutors_signed_up = User.objects.filter(profile = UserProfile.TYPES.TUTOR) \
                        .filter(date_joined__year = year).count()
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year)
    
    else:
        tutors_signed_up = User.objects.filter(profile = UserProfile.TYPES.TUTOR).count()
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING])
    
    
    price_per_hour = init_price_per_hour()
    total_price = init_total_price()
    class_time = init_class_time()
    
    system = OrderedDict()
    subject = OrderedDict()
    level = OrderedDict()
    subject_level = OrderedDict()
    users = set()
    
    for class_ in classes:
        add_tutor_to_dict(class_time, '%s minutes' % class_.duration, class_)
        if class_.system: add_tutor_to_dict(system, '%s' % class_.system, class_)
        if class_.level: add_tutor_to_dict(level, '%s' % class_.level, class_)
        if class_.only_subject: add_tutor_to_dict(subject, '%s' % class_.only_subject, class_)
        add_tutor_to_dict(subject_level, '%s' % class_.subject, class_)
        add_tutor_to_dict(price_per_hour, get_price_per_hour_slot(class_), class_)
        add_tutor_to_dict(total_price, get_total_price_slot(class_), class_)
        users.add(class_.tutor.username)
    
    return {
        'price_per_hour': price_per_hour,
        'total_price': total_price,
        'class_time': class_time,
        'system': system,
        'level': level,
        'subject': subject,
        'subject_level': subject_level,
        'total_tutors': User.objects.filter(profile__type = UserProfile.TYPES.TUTOR).count(),
        'tutors_taking_classes': len(users),
        'tutors_signed_up': tutors_signed_up,
        'years': [(y,y) for y in reversed(range(2012, today.year + 1))],
        'months': [(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),
                  (7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December'),],
        'days': [(d,d) for d in range(1, 32)],
        'day': day,
        'month': month,
        'year': year,
    }


@main_render(template='core/reports/classes.html')
def reports_classes(request):
    user = request.user

    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()
    
    today = datetime.datetime.today()
    
    year = int(request.GET.get('year', 0) or 0)
    month = int(request.GET.get('month', 0) or 0)
    day = int(request.GET.get('day', 0) or 0)
    
    if year and month and day:
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year, date__month = month, date__day = day)
        
    elif year and month:
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year, date__month = month)
    
    elif year:
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING]) \
                        .filter(date__year = year)
    
    else:
        classes = Class.objects.select_related() \
                        .exclude(status__in = [Class.STATUS_TYPES.PRE_BOOKED, Class.STATUS_TYPES.WAITING])
    
    
    price_per_hour = init_price_per_hour()
    total_price = init_total_price()
    class_time = init_class_time()
    
    system = OrderedDict()
    subject = OrderedDict()
    level = OrderedDict()
    subject_level = OrderedDict()
    class_status = [0 for i in xrange(10)]
    
    for class_ in classes:
        add_class_to_dict(class_time, '%s minutes' % class_.duration, class_)
        if class_.system: add_class_to_dict(system, '%s' % class_.system, class_)
        if class_.level: add_class_to_dict(level, '%s' % class_.level, class_)
        if class_.only_subject: add_class_to_dict(subject, '%s' % class_.only_subject, class_)
        add_class_to_dict(subject_level, '%s' % class_.subject, class_)
        add_class_to_dict(price_per_hour, get_price_per_hour_slot(class_), class_)
        add_class_to_dict(total_price, get_total_price_slot(class_), class_)
        class_status[class_.status] += 1
    
    return {
        'price_per_hour': price_per_hour,
        'total_price': total_price,
        'class_time': class_time,
        'system': system,
        'level': level,
        'subject': subject,
        'subject_level': subject_level,
        'class_status': class_status,
        'years': [(y,y) for y in reversed(range(2012, today.year + 1))],
        'months': [(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),
                  (7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December'),],
        'days': [(d,d) for d in range(1, 32)],
        'day': day,
        'month': month,
        'year': year,
    }


@main_render(template='core/reports/financial.html')
def reports_financial(request):
    user = request.user

    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()
    
    today = datetime.datetime.today()
    
    year = int(request.GET.get('year', 0) or 0)
    month = int(request.GET.get('month', 0) or 0)
    day = int(request.GET.get('day', 0) or 0)
    
    TYPES = UserCreditMovement.MOVEMENTS_TYPES
    
    if year and month and day:
        items = UserCreditMovement.objects.filter(type__in = [TYPES.WITHDRAW, TYPES.TOPUP]) \
                        .filter(created__year = year, created__month = month, created_day = day) \
                        .order_by('created')
        classes = Class.objects.select_related() \
                        .filter(status = Class.STATUS_TYPES.DONE, date__year = year, date__month = month, date__day = day).order_by('date')
  
    elif year and month:
        items = UserCreditMovement.objects.filter(type__in = [TYPES.WITHDRAW, TYPES.TOPUP]) \
                        .filter(created__year = year, created__month = month) \
                        .order_by('created')
        classes = Class.objects.select_related() \
                        .filter(status = Class.STATUS_TYPES.DONE, date__year = year, date__month = month).order_by('date')
    
    elif year:
        items = UserCreditMovement.objects.filter(type__in = [TYPES.WITHDRAW, TYPES.TOPUP]) \
                        .filter(created__year = year) \
                        .order_by('created')
        classes = Class.objects.select_related() \
                        .filter(status = Class.STATUS_TYPES.DONE, date__year = year).order_by('date')
    
    else:
        items = UserCreditMovement.objects.filter(type__in = [TYPES.WITHDRAW, TYPES.TOPUP]).order_by('created')
        classes = Class.objects.select_related().filter(status = Class.STATUS_TYPES.DONE).order_by('date')
    
    topup_credits = 0
    withdraw_credits = 0
    profit_credits = 0
    
    unused_credits = 0
    credits_to_withdraw = 0
    currencies_to_withdraw = init_currencies()
    
    currencies = init_currencies()
    credits_evolution = init_credits_evolution(items, classes)

    for item in items:
        symbol, value = item.value.split()
        value = float(value)
        if item.type == TYPES.TOPUP:
            currencies[symbol]['topup'] += value
            credits_evolution[item.created.strftime('%b %Y')]['topup'] += value
            topup_credits += item.credits
        if item.type == TYPES.WITHDRAW:
            currencies[symbol]['withdraw'] += value
            credits_evolution[item.created.strftime('%b %Y')]['withdraw'] += value
            withdraw_credits += item.credits

    for class_ in classes:
        profit_credits += class_.universal_fee
        credits_evolution[class_.date.strftime('%b %Y')]['profit'] += class_.universal_fee
    
    for profile in UserProfile.objects.select_related().filter(type__in = [UserProfile.TYPES.TUTOR, UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16]):
        if profile.type == UserProfile.TYPES.TUTOR:
            credits_to_withdraw += profile.income
            currency = profile.currency
            currencies_to_withdraw[currency.symbol]['withdraw'] += profile.income         
        if profile.type in [UserProfile.TYPES.STUDENT, UserProfile.TYPES.UNDER16]:
            unused_credits += profile.credit
        
    return {
        'topup_credits': topup_credits,
        'withdraw_credits': withdraw_credits,
        'profit_credits': profit_credits,

        'unused_credits': unused_credits,
        'credits_to_withdraw': credits_to_withdraw,

        'currencies': currencies,
        'currencies_to_withdraw': currencies_to_withdraw,
        'credits_evolution': credits_evolution,
        
        'years': [(y,y) for y in reversed(range(2012, today.year + 1))],
        'months': [(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),
                  (7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December'),],
        'days': [(d,d) for d in range(1, 32)],
        'day': day,
        'month': month,
        'year': year,
    }

































### MONITORING ############################################################
###########################################################################
@main_render('core/monitoring/classes.html')
def monitoring_classes(request):
    """
    detailed profile from a user
    """
    user = request.user

    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()

    classes =  Class.objects.raw(
        """
        SELECT *
        FROM classes_class
        WHERE status = %(booked)s
          AND date <= CURRENT_TIMESTAMP
          AND date + (duration || ' minutes')::interval >= CURRENT_TIMESTAMP
        ORDER BY date ASC
        """ % {
            'booked': Class.STATUS_TYPES.BOOKED,
    })

    return {
        'classes': classes,
    }
    
@main_render('core/monitoring/class.html')
def monitoring_class(request, class_id):
    """
    detailed profile from a user
    """
    user = request.user

    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()

    try:
        class_ = Class.objects.select_related().get(id = class_id)
    except Class.DoesNotExist:
        raise http.Http404()

    scribblar_user = get_invisible_user()

    return {
        'class': class_,
        'scribblar_user': scribblar_user,
    }


@main_render('core/profile/waiting_approval.html')
def waiting_approval(request):
    """
    detailed profile from a user
    """
    user = request.user

    if not user.is_authenticated() or not user.is_superuser:
        raise http.Http404()

    return {
        'users': User.objects.select_related().filter(
                    Q(profile__type = UserProfile.TYPES.TUTOR),
                    Q(profile__profile_image_approved=False) |
                    Q(profile__about_approved=False) |
                    Q(profile__video_approved=False) |
                    Q(profile__qualification_documents_approved=False)
                ).distinct(),
    }