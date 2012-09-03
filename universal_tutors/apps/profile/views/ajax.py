import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import http
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.files import File
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.conf import settings

from filebrowser.templatetags.fb_versions import VersionNode

from apps.profile.models import *
from apps.profile.forms import *
from apps.profile.utils import *
from apps.classes.models import ClassSubject
from apps.common.utils.view_utils import main_render, handle_uploaded_file
from apps.common.utils.date_utils import convert_datetime
from apps.core.models import Discount

import pytz, datetime, os, string, random
import base64
import cStringIO

try:
    import simplejson
except ImportError:
    from django.utils import simplejson


@csrf_exempt
def add_newsletter_subscription(request):
    if request.method == "POST":
        form = NewsletterSubscribeForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            created = False

            if user:
                youcoca_user = True
                user.profile.newsletters = True
                user.save()
            else:
                youcoca_user = False
                _, created = NewsletterSubscription.objects.get_or_create(email=email)
            return HttpResponse(simplejson.dumps({'success': True, 'youcoca_user': youcoca_user, 'created': created}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'success': False}), content_type='application/json')


@login_required
def view_modal_messages(request, username, to, class_id=0):
    user = request.user

    if username:
        person = get_object_or_404(User, username = username)
        if person != user and person.profile.parent != user:
            raise http.Http404()
    elif user.is_authenticated():
        person = user
    else:
        raise http.Http404()
        
    to = get_object_or_404(User, id=to)
    to_profile = to.profile
    class_id = int(class_id)
    
    person_profile = person.profile
    
    if class_id:
        try:
            class_ = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            raise http.Http404()
    
        messages = Message.objects.select_related().filter(Q(related_class=class_), Q(user=person, to=to) | Q(user=to, to=person))
    else:
        messages = Message.objects.select_related().filter(Q(user=person, to=to) | Q(user=to, to=person))

    messages.filter(to=user).update(read=True)

    message_list = []
    for message in messages:
        child = ''
        parent = ''
        child_type = ''
        if person_profile.type == person_profile.TYPES.TUTOR and person == message.to:
            message_profile = message.user.profile
            if message_profile.type == message_profile.TYPES.PARENT:
                child = message.child.get_full_name()
            elif message_profile.type == message_profile.TYPES.UNDER16:
                parent = message_profile.parent.get_full_name()
                child_type = message_profile.child_type
        
        message_list.append({
                'to_id': message.to.id,
                'to': message.to.get_full_name(),
                'user_id': message.user.id,
                'user': message.user.get_full_name(),
                'text': message.message,
                'child': child,
                'parent': parent,
                'child_type': child_type,
            })
    
    data = json.dumps({
        'to': to.get_full_name(), 
        'messages': message_list,
    })
    
    return http.HttpResponse(data, mimetype='application/json')


@login_required
def send_modal_message(request, to, class_id=0):
    user = request.user
    user_profile = user.profile
    to = get_object_or_404(User, id=to)
    class_id = int(class_id)
    
    if request.method != 'POST':
        return http.HttpResponseForbidden()
    
    profile = to.profile
    if (profile.type == profile.TYPES.STUDENT or profile.type == profile.TYPES.UNDER16) and \
       not Message.objects.filter(Q(user=to, to=user) | Q(user=user, to=to)) and \
       not user.classes_as_tutor.filter(student=to) and not profile.parent == user:
        raise http.Http404()
    
    text = request.POST.get('modal-message-text')
    child = None
    if user_profile.type == user_profile.TYPES.PARENT:
        try:
            child = User.objects.select_related().get(id=request.POST.get('child', 0))
            profile = child.profile
        except User.DoesNotExist:
            return http.HttpResponse("Please select one of your children.") 
    
    if class_id:
        try:
            class_ = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            raise http.Http404()
    
        Message.objects.create(user=user, to=to, related_class=class_, message=text, child=child)
    else:
        Message.objects.create(user=user, to=to, message=text, child=child)
    
    return http.HttpResponseRedirect(reverse('view_modal_messages', args=[user.username, to.id, class_id]))


@login_required
def tutor_cancel_class(request):
    user = request.user
    
    if request.method != 'POST':
        raise http.Http404()
        
    class_id = request.POST.get('class_id')
    reason = request.POST.get('reason')
    
    try:
        class_ = Class.objects.get(id=class_id, tutor=user, status=Class.STATUS_TYPES.BOOKED)
    except Class.DoesNotExist:
        raise http.Http404()
        
    class_.canceled_by_tutor(reason)
        
    return http.HttpResponse('done.')


@login_required
def student_cancel_class(request):
    user = request.user

    if request.method != 'POST':
        raise http.Http404()
        
    class_id = request.POST.get('class_id')
    reason = request.POST.get('reason')
    
    try:
        class_ = Class.objects.get(id=class_id, student=user)
    except Class.DoesNotExist:
        raise http.Http404()
    
    cancelation_time = datetime.datetime.now() - datetime.timedelta(minutes = 5 if class_.duration < 60 else 10)
    
    if class_.date < cancelation_time:
        return http.HttpResponse('Grace period is over.')
        
    class_.canceled_by_student(reason)
    return http.HttpResponse('done.')


@login_required
def tutor_rate_student(request):
    user = request.user

    if request.method != 'POST':
        raise http.Http404()
        
    class_id = request.POST.get('class_id')
    user_id = request.POST.get('user_id')
    text = request.POST.get('text')
    
    try:
        class_ = Class.objects.get(id=class_id, tutor=user)
    except Class.DoesNotExist:
        raise http.Http404()

    try:
        student = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise http.Http404()
    
    
    if student != class_.student:
        raise http.Http404()
    
    try:
        review = student.reviews_as_student.get(related_class = class_)
        review.text = text
        review.save()
    except StudentReview.DoesNotExist:
        student.reviews_as_student.create(related_class = class_, text = text)
        
    if class_.status == class_.STATUS_TYPES.BOOKED:
        class_.done()
    
    return http.HttpResponse('done.')


@login_required
def student_rate_tutor(request):
    user = request.user

    if request.method != 'POST':
        raise http.Http404()
        
    class_id = request.POST.get('class_id')
    user_id = request.POST.get('user_id')
    rate = int(request.POST.get('rate'))
    text = request.POST.get('text')
    
    try:
        class_ = Class.objects.get(Q(id=class_id), Q(student=user) | Q(student__parent_set__parent=user, student__parent_set__active=True))
    except Class.DoesNotExist:
        raise http.Http404()

    try:
        tutor = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise http.Http404()
    
    
    if tutor != class_.tutor:
        raise http.Http404()
    
    try:
        review = tutor.reviews_as_tutor.get(related_class = class_)
        review.text = text
        review.rate = rate
        review.save()
    except TutorReview.DoesNotExist:
        tutor.reviews_as_tutor.create(related_class = class_, text = text, rate = rate)
        
    
    if class_.status == class_.STATUS_TYPES.BOOKED:
        class_.done()
    
    return http.HttpResponse('done.')


@login_required
def favorite(request, person_id):
    user = request.user

    try:
        person = User.objects.select_related().get(id=person_id)
    except User.DoesNotExist:
        raise http.Http404()
    
    profile = person.profile
    
    if user in profile.favorite.all():
        profile.favorite.remove(user)
        return http.HttpResponse('Add favorite')
    else:
        profile.favorite.add(user)
        return http.HttpResponse('Remove favorite')


@login_required
def add_interest(request):
    user = request.user

    interest = request.GET.get('interest', None)
    if not interest:
        raise http.Http404()
    
    try:
        subject = ClassSubject.objects.get(subject__iexact=interest)
    except ClassSubject.DoesNotExist:
        subject = ClassSubject.objects.create(subject=interest)
    
    user.profile.interests.add(subject)
    return http.HttpResponse('%s' % subject.id)


@login_required
def remove_interest(request, subject_id):
    user = request.user

    try:
        subject = ClassSubject.objects.get(id=subject_id)
        user.profile.interests.remove(subject)
    except ClassSubject.DoesNotExist:
        pass
    
    return http.HttpResponse('done')


@login_required
def referral_friend(request):
    user = request.user

    if request.method != 'POST':
        raise http.Http404()

    form = ReferralForm(request.POST)
    if form.is_valid():
        referral = form.save(commit = False)
        referral.user = user
        referral.save()
        
        return http.HttpResponse('done')
    
    return http.HttpResponse('error')



#### AVAILABILITY ###########################################################
#############################################################################
@login_required
@main_render('profile/tutor/edit_profile/availability/_new_period.html')
def edit_week_period(request, period_id, begin, end, weekday):
    user = request.user

    try:
        availability = user.week_availability.get(id=period_id)
        new_object = False;
    except WeekAvailability.DoesNotExist:
        availability = WeekAvailability()
        availability.user = user
        availability.weekday = int(weekday)
        new_object = True

    try:
        begin_array = begin.split('-')
        begin_time = datetime.time(int(begin_array[0]), int(begin_array[1]) / MINIMUM_PERIOD * MINIMUM_PERIOD)
        end_array = end.split('-')
        end_time = datetime.time(int(end_array[0]), int(end_array[1]) / MINIMUM_PERIOD * MINIMUM_PERIOD)
    except IndexError:
        raise http.Http404()

    availability.begin = begin_time
    availability.end = end_time
    availability.save()

    if new_object:
        if availability.id:
            return { 'period': availability, }
        raise http.Http404()
    else:
        return http.HttpResponse('done.')

@login_required
def delete_week_period(request, period_id):
    user = request.user

    availability = get_object_or_404(WeekAvailability, id = period_id, user=user)
    availability.delete()

    return http.HttpResponse('done.')
    

@login_required
@main_render('profile/tutor/edit_profile/availability/this_weekday_calendar.html')
def view_week_period(request, date=None):
    user = request.user

    if date:
        try:
            date_str = date.split('-')
            date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        except:
            date = datetime.date.today()
    else:
        date = datetime.date.today()

    date = first_day_of_week(date)
    today = datetime.date.today()
    nxt_month = next_month(date)
    prv_month = prev_month(date)
    months = [to_calendar(date), to_calendar(nxt_month)]

    return {
        'home': True,
        'months': months,
        'today': today,
        'next_month': nxt_month,
        'prev_month': prv_month,

        'this_week': user.profile.get_this_week(date),
        'prev_week': date - datetime.timedelta(days=7),
        'next_week': date + datetime.timedelta(days=7),
        'first_day_of_week': date,
    }
    

@login_required
@main_render('profile/tutor/edit_profile/availability/_this_week_day_periods.html')
def edit_this_week_period(request, date, type, period_id, begin, end, weekday):
    user = request.user
    type = int(type)

    try:
        date_str = date.split('-')
        date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        date = date + datetime.timedelta(days = int(weekday))
    except:
        raise http.Http404()

    if type == Profile.AVAILABILITY_TYPES.CUSTOM_DAY:
        try:
            availability = user.day_availability.objects.get(id=period_id)
        except DayAvailability.DoesNotExist:
            if not user.day_availability.filter(date = date):
                week_availability = user.day_availability.filter(weekday=weekday)
                for a in week_availability:
                    availability = DayAvailability()
                    availability.user = user
                    availability.date = date
                    availability.begin = a.begin
                    availability.end = a.end
                    availability.save()
            
            availability = DayAvailability()
            availability.user = user
            availability.date = date
            new_object = True
    else: 
        week_availability = user.week_availability.filter(weekday=weekday).exclude(id = period_id)
        for a in week_availability:
            availability = DayAvailability()
            availability.user = user
            availability.date = date
            availability.begin = a.begin
            availability.end = a.end
            availability.chairs = a.chairs
            availability.save()
        
        availability = DayAvailability()
        availability.user = user
        availability.date = date
        new_object = True

    try:
        begin_array = begin.split('-')
        begin_time = datetime.time(int(begin_array[0]), int(begin_array[1]) / MINIMUM_PERIOD * MINIMUM_PERIOD)
        end_array = end.split('-')
        end_time = datetime.time(int(end_array[0]), int(end_array[1]) / MINIMUM_PERIOD * MINIMUM_PERIOD)
    except IndexError:
        raise http.Http404()

    availability.begin = begin_time
    availability.end = end_time
    availability.save()

    type, periods = user.profile.get_day_periods(date)

    if new_object:
        if availability.id:
            return {
                'type': type,
                'periods': periods,
                'date': date,
            }
        raise http.Http404()
    else:
        return http.HttpResponse('done.')


@login_required
@main_render('profile/tutor/edit_profile/availability/_this_week_day_periods.html')
def delete_this_week_period(request, period_id):
    user = request.user

    availability = get_object_or_404(DayAvailability, id = period_id, user=user)
    date = availability.date
    availability.delete()

    type, periods = user.profile.get_day_periods(date)

    return {
        'type': type,
        'periods': periods,
        'date': date,
    }


@login_required
def book_class(request, tutor_id):
    user = request.user
    profile = user.profile
    
    if request.method != 'POST' or profile.type == profile.TYPES.TUTOR:
        raise http.Http404()
    
    subject_id = request.POST.get('subject', 0)
    date = request.POST.get('date', '')
    start = request.POST.get('start', '')
    duration = int(request.POST.get('duration', 0))
    cover = request.POST.get('cover', None)
    message = request.POST.get('message', None)
    child_id = request.POST.get('child', 0)

    if profile.type == profile.TYPES.PARENT:
        try:
            child = User.objects.select_related().get(id=child_id)
            profile = child.profile
            if profile.parent == user:
                user = child
            else:
                raise http.Http404()
        except User.DoesNotExist:
            return http.HttpResponse("Please select one of your children.") 

    if duration < 30 or duration > 120 or (duration % 30 != 0):
        raise http.Http404()

    try:
        tutor = User.objects.select_related().get(id=tutor_id, profile__type=UserProfile.TYPES.TUTOR)
    except User.DoesNotExist:
        raise http.Http404()

    try:
        subject = tutor.subjects.get(id=subject_id)
    except TutorSubject.DoesNotExist:
        raise http.Http404()

    try:
        date_str = date.split('-')
        date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        start_array = start.split('-')
        start_time = datetime.time(int(start_array[0]), int(start_array[1]) / MINIMUM_PERIOD * MINIMUM_PERIOD)
    except ValueError:
        raise http.Http404()
    except IndexError:
        raise http.Http404()

    
    date = datetime.datetime.combine(date, start_time)
    date = convert_datetime(date, profile.timezone, pytz.utc)
    
    class_ = Class(
        tutor = tutor,
        student = user,
        subject = '%s' % subject,
        only_subject = '%s' % subject.subject,
        level = '%s' % subject.level,
        system = '%s' % subject.system,
        subject_credits_per_hour = subject.credits,
        date = date,
        duration = duration,
        cover = cover,
    )

    credit_fee = class_.get_updated_credit_fee(commit=False)
    if credit_fee > profile.credit:
        return http.HttpResponse("You don't have enough credits.")
    
    class_.save()    
    if not class_.id:
        return http.HttpResponse("This class can't be created right now. Please try again later.")    
    class_.book()

    if message:
        user.sent_messages.create(
            to = tutor,
            message = message,
            related_class = class_,
            read = False,
            email_sent = False,
        )

    return http.HttpResponse("Done.")


@login_required
def set_class_language(request, language):
    profile = request.user.profile
    profile.class_language = language
    profile.save()
    
    return http.HttpResponse('Done.')

@csrf_exempt
def send_parent_request(request):
    if request.POST:
        try:
            email = request.POST.get('email')
            template = loader.get_template('emails/parent_request.html')
            context = Context({
                'PROJECT_SITE_DOMAIN': settings.PROJECT_SITE_DOMAIN,
            })
            html = template.render(context)
    
            msg = EmailMessage(
                               'New Contact Message', 
                               html, 
                               settings.DEFAULT_FROM_EMAIL, 
                               [email])
            msg.content_subtype = 'html'
            msg.send()
            
            return http.HttpResponse("Email sent successfully");
        except:
            return http.HttpResponseServerError("An error occurred while sending the email.");
    else:
        return http.HttpResponseBadRequest()


@login_required
@main_render('account/signup.html')
def add_child(request):
    user = request.user
    profile = user.profile
    
    if profile.type != profile.TYPES.PARENT:
        raise http.Http404()

    form = SignupForm(request.POST or None, parent=user)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(request=request)
            return http.HttpResponse('child_created')
    
    return {
        'form': form,
        'child_creator': True,
    }


@login_required
@main_render('profile/tutor/book_class/_new_week_calendar.html')
def ajax_book_class(request, username, date):
    """
    view my recent activity
    """
    user = request.user
    tutor = get_object_or_404(User, username = username, profile__type = UserProfile.TYPES.TUTOR)
    profile = tutor.profile
    
    try:
        date_str = date.split('-')
        date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        date = date - datetime.timedelta(days=date.weekday())
    except IndexError:
        raise http.Http404()

    return {
        'person': tutor,
        'profile': profile,
        'week': profile.get_week(date, gtz = user.profile.timezone),
        'date': date,
    }


@main_render()
def ajax_week_classes(request, date, is_tutor = 0):
    """
    view my recent activity
    """
    user = request.user
    
    try:
        date_str = date.split('-')
        date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        date = date - datetime.timedelta(days=date.weekday())
    except IndexError:
        raise http.Http404()

    if int(is_tutor):
        template = 'profile/tutor/edit_profile/classes/_new_weekday_calendar.html'
    else:
        template = 'profile/student/edit_profile/classes/_new_weekday_calendar.html'

    return {
        'TEMPLATE': template,
        'person': user,
        'profile': user.profile,
        'date': date,
    }


@login_required
def add_credits(request, username=None):
    ###
    ### DUMMY, TO DELETE AFTER
    ###
    if username:
        user = request.user
        person = get_object_or_404(User, username=username)
        profile = person.profile
        if user != person and profile.parent != user:
            raise http.Http404()
    else:
        person = request.user
        profile = person.profile

    profile.topup_account(30)
    
    return http.HttpResponse('done')


@login_required
def accept_class(request, class_id):
    user = request.user
    
    try:
        class_ = Class.objects.get(id=class_id, tutor=user, status=Class.STATUS_TYPES.WAITING)
    except Class.DoesNotExist:
        raise http.Http404()
    
    class_.accept()

    return http.HttpResponse('done.')

@login_required
def reject_class(request):
    user = request.user
    
    if request.method != 'POST':
        raise http.Http404()
        
    class_id = request.POST.get('class_id', 0)
    reason = request.POST.get('reason', '')
    
    try:
        class_ = Class.objects.get(id=class_id, tutor=user, status=Class.STATUS_TYPES.WAITING)
    except Class.DoesNotExist:
        raise http.Http404()
        
    class_.reject(reason)
        
    return http.HttpResponse('done.')

@login_required
def check_tutor_class_status(request):
    user = request.user
    profile = user.profile
    
    if profile.type != profile.TYPES.TUTOR:
        raise http.Http404()

    if profile.test_class_minutes:
        profile.test_class_minutes -= 1
        super(UserProfile, profile).save()
        
        if profile.test_class_minutes:
            return http.HttpResponse('ok')
        else:
            return http.HttpResponse('close')


def get_user_data(request, user_id):
    try:
        user = User.objects.select_related().get(id=user_id)
    except User.DoesNotExist:
        raise http.Http404()
    
    image = 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, user.profile.profile_image.url)
    url = 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, reverse('profile', args=[user.username]))
    
    return http.HttpResponse('%s,%s' % (image, url))


@login_required
def update_header(request):
    profile = UserProfile.objects.select_related().get(user = request.user)
    
    data = json.dumps({
        'new_classes': profile.new_classes() if profile.type == profile.TYPES.TUTOR else 0,
        'no_messages': profile.no_messages(), 
    })
    
    return http.HttpResponse(data, mimetype='application/json')


@login_required
def activate_discount(request):
    if not request.method == 'POST':
        raise http.Http404()
    
    user = request.user
    profile = user.profile
    code = request.POST.get('discount', '')
    
    if not code:
        raise http.Http404()
    
    try:
        if profile.type == profile.TYPES.TUTOR:
            discount = Discount.objects.get(code=code, type__in=[Discount.TYPES.ALL, Discount.TYPES.TUTOR])
        elif profile.type == profile.TYPES.PARENT:
            discount = Discount.objects.get(code=code, type__in=[Discount.TYPES.ALL, Discount.TYPES.PARENT])
        else:
            discount = Discount.objects.get(code=code, type__in=[Discount.TYPES.ALL, Discount.TYPES.STUDENT])
            
    except Discount.DoesNotExist:
        return http.HttpResponse('Invalid discount code!')
    
    user_discount, created = user.discounts.get_or_create(discount=discount)
    user.discounts.exclude(id=user_discount.id).update(active=False)
    if user_discount.activate():
        return http.HttpResponse('done.')
    else:
        return http.HttpResponse('This discount code has expired!')

@csrf_exempt
def preview_profile_image(request):
    if not request.method == 'POST':
        raise http.Http404()
    
    upload = request
    is_raw = True
    try:
        filename = request.GET[ 'qqfile' ]
    except KeyError: 
        return HttpResponseBadRequest( "AJAX request not valid" )
     

    name, ext = os.path.splitext(filename)
    name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
    new_filename = '%s%s' % (name, ext.lower())
    filename = os.path.join(settings.MEDIA_ROOT, UploadProfileImage.UPLOAD_IMAGES_PATH, new_filename)
    success = save_upload( upload, filename, is_raw )
  
    image, created = UploadProfileImage.objects.get_or_create(key=request.session.session_key)
    image.image = File(open(filename))
    image.save()
 
    import json
    ret_json = { 'url': image.image.url }
    return HttpResponse( json.dumps( ret_json ) )


@csrf_exempt
def preview_profile_image_delete(request):
    UploadProfileImage.objects.filter(key=request.session.session_key).update(image=None)
    UploadProfileImage.objects.filter(key=request.session.session_key).delete()
    return http.HttpResponse('done.')
