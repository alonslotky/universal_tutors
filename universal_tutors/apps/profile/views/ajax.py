from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import http
from django.http import HttpResponse
from django.contrib.auth.models import User

from apps.profile.models import NewsletterSubscription
from apps.profile.forms import *
from apps.common.utils.view_utils import main_render, handle_uploaded_file

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
@main_render('profile/iframes/change_photo.html')
def change_photo(request):

    form = ProfilePhotoForm(request.POST or None, request.FILES or None)

    success = False
    error_message = ''

    photo = ''

    if request.method == 'POST' and form.is_valid():
        user = request.user
        profile = user.profile

        f, filename = handle_uploaded_file(request.FILES['photo'], 'uploads/profiles/profile_images')

        profile.profile_image = 'uploads/profiles/profile_images/' + filename
        profile.save()

        success = True

        photo = profile.get_profile_image_path()

    return {
        'success': success,
        'form': form,
        'photo': photo,
    }




#### AVAILABILITY ###########################################################
#############################################################################
@login_required
@main_render('profile/tutor/edit_profile/availability/_week_period.html')
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


