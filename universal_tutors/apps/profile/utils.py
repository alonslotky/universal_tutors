import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from apps.core.models import Currency
from apps.profile.models import Tutor, WithdrawItem
from paypal2.standart.ap import pay

def mass_payments():
    notify_url = 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, reverse('paypal-ipn')),
    for currency in Currency.objects.all():
        credit_value = currency.credit_value()
        tutors = Tutor.objects.select_related().filter(
                    profile__currency = currency, 
                    profile__income__gt = 0, 
                    profile__paypal_email__isnull=False,
                ).exclude(profile__paypal_email = '')
        
        receivers = []
        for user in tutors:
            profile = user.profile
            credits = profile.income
            amount = credits * credit_value
            email = profile.paypal_email
            withdraw = WithdrawItem(
                user = user,
                value = amount,
                credits = credits, 
                email = email,
                currency = currency,
            )
            withdraw.save()
        
            receivers.append({
                'email': email, 
                'amount': '%.2f' % amount,
                'unique_id': 'wd-%s' % withdraw.id,
            })
        
        if receivers:
            pay({
                'notify_url': notify_url,
                'currencyCode': currency.acronym,
                'receivers': receivers,
            })


def check_crb():
    for tutor in Tutor.objects.select_related().filter(profile__crb_expiry_date__isnull = False):
        tutor.profile.check_crb()
        