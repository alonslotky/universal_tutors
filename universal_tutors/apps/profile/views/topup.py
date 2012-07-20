import simplejson as json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import http
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.conf import settings

from paypal.standard.forms import PayPalPaymentsForm
from apps.common.utils.view_utils import main_render, handle_uploaded_file
from apps.profile.models import TopUpItem
from apps.core.models import Bundle

try:
    import simplejson
except ImportError:
    from django.utils import simplejson


@login_required
def withdraw(request):
    user = request.user
    profile = user.profile
    
    if profile.type != profile.TYPES.TUTOR or request.method != 'POST':
        raise http.Http404()
        
    profile.process_manual_withdraw()
    
    return http.HttpResponse('done.')


@login_required
@main_render()
def topup_cart(request, username=None):
    user = request.user
    
    if username:
        person = get_object_or_404(User, username=username)
        if person != user and person.profile.parent != user:
            raise http.Http404()
    else:
        person = user

    profile = user.profile
    currency = profile.currency    

    form = None 
    topup = None
    if request.method == "POST":
        credits = int(round(float(request.POST.get('credits', 0))))
        try:
            bundle = Bundle.objects.filter(credits__lte = credits).order_by('-credits')[0]
            value = round(credits * currency.credit_value() * (1 - bundle.discount), 2)
        except IndexError:
            value = round(credits * currency.credit_value(), 2)

        if credits:
            topup = TopUpItem(user=person, credits=credits, value=value, currency=currency)
            topup.save()
    else:
        try:
            person.topups.filter(status = TopUpItem.STATUS_TYPES.CART).latest('id').delete()
        except TopUpItem.DoesNotExist:
            pass
    
    if topup:
        form = PayPalPaymentsForm(initial = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "item_name": "Top-up %s's account" % (person.get_full_name(), ),
            "item_number": topup.id,
            "invoice": topup.invoice,
            "notify_url": "http://%s%s" % (settings.PROJECT_SITE_DOMAIN, reverse('paypal-ipn')), 
            "return_url": "http://%s%s" % (settings.PROJECT_SITE_DOMAIN, reverse('topup_successful', args=[person.username])),
            "cancel_return": "http://%s%s" % (settings.PROJECT_SITE_DOMAIN, reverse('topup_cancel', args=[person.username])),
            "amount": topup.value,
            "currency_code": topup.currency.acronym,
        })
        template = 'profile/student/edit_profile/fragments/_modal_topup_cart.html'
    else:
        template = 'profile/student/edit_profile/fragments/_modal_topup_add_to_cart.html'
   
    return {
        'TEMPLATE': template,
        'form': form,
        'person': person,
        'profile': profile,
        'currency': currency,
        'topup': topup,
        'bundles': Bundle.objects.all(),
    }

@login_required
@main_render('profile/student/edit_profile/fragments/_modal_topup_add_to_cart.html')
def topup_cancel(request, username, ajax=0):
    user = request.user
    profile = user.profile
    ajax = int(ajax)
    
    if username:
        person = get_object_or_404(User, username=username)
        if person != user and person.profile.parent != user:
            raise http.Http404()
    else:
        person = user

    try:
        topup = person.topups.filter(status = TopUpItem.STATUS_TYPES.CART).latest('id')
        topup.cancel()
    except TopUpItem.DoesNotExist:
        pass
    
    if ajax:
        return {
            'person': person,
            'currency': profile.currency,
            'bundles': Bundle.objects.all(),
        }
    else:
        if profile.type == profile.TYPES.STUDENT:
            return http.HttpResponseRedirect('%s#credits' % reverse('edit_student_profile'))
        else:
            return http.HttpResponseRedirect('%s#children' % reverse('edit_parent_profile'))
    

@csrf_exempt
@main_render('profile/student/successfull_topup.html')
def topup_successful(request, username):
    user = request.user
    profile = user.profile
    
    if username:
        person = get_object_or_404(User, username=username)
        if person != user and person.profile.parent != user:
            raise http.Http404()
    else:
        person = user

    return {
        'person': person
    }
