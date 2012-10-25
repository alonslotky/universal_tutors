import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from apps.core.models import Currency
from apps.profile.models import Tutor, WithdrawItem, Message
from paypal.standard.ap import adaptive_payment

try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict


def mass_payments(single_tutor = None):
    notify_url = 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, reverse('paypal-ipn')),
    
    for currency in Currency.objects.all():
        credit_value = currency.credit_value()
        
        if single_tutor:
            tutors = Tutor.objects.select_related().filter(
                        id = single_tutor.id,
                        profile__currency = currency, 
                        profile__income__gt = 0, 
                        profile__paypal_email__isnull=False,
                    ).exclude(profile__paypal_email = '')
        else:
            tutors = Tutor.objects.select_related().filter(
                        profile__currency = currency, 
                        profile__income__gt = 0, 
                        profile__paypal_email__isnull=False,
                    ).exclude(profile__paypal_email = '')
        
        receivers = []
        withdraws = []
        
        for user in tutors:
            profile = user.profile
            credits = profile.income
            amount = round(credits * credit_value, 2)
            email = profile.paypal_email
            withdraw = WithdrawItem(
                user = user,
                value = amount,
                credits = credits, 
                email = email,
                currency = currency,
            )
            withdraw.save()
            withdraws.append(withdraw)
        
            receivers.append({
                'email': email,
                'name': user.get_full_name(),
                'amount': '%.2f' % amount,
                'invoiceId': 'WD-%s' % withdraw.id,
                'customId': 'WD-%s' % withdraw.id,
            })

        if receivers:
            payment = {
                'currencyCode': currency.acronym,
                'feesPayer': 'EACHRECEIVER' if single_tutor else 'SENDER',
                'memo': 'Universal Tutors Payment',
            }

            for i, receiver in enumerate(receivers):
                payment['receiverList.receiver(%s).amount' % i] = receiver['amount']
                payment['receiverList.receiver(%s).email' % i] = receiver['email']
                payment['receiverList.receiver(%s).name' % i] = receiver['name']
                payment['receiverList.receiver(%s).invoiceId' % i] = receiver['invoiceId']
    
            if not adaptive_payment(payment).get('paykey', None):
                for withdraw in withdraws:
                    withdraw.cancel()
            

def check_crb(user_thread=True):
    for tutor in Tutor.objects.select_related().filter(profile__crb_expiry_date__isnull = False):
        tutor.profile.check_crb(user_thread)


def send_message_email(use_thread=True):
    now = datetime.datetime.now() - datetime.timedelta(minutes=1)
    for message in Message.objects.select_related().filter(created__lte=now, read=False, email_sent=False):
        message.send_email(use_thread)


def save_upload( uploaded, filename, raw_data ):
  ''' 
  raw_data: if True, uploaded is an HttpRequest object with the file being
            the raw post data 
            if False, uploaded has been submitted via the basic form
            submission and is a regular Django UploadedFile in request.FILES
  '''
  try:
    from io import FileIO, BufferedWriter
    with BufferedWriter( FileIO( filename, "wb" ) ) as dest:
      # if the "advanced" upload, read directly from the HTTP request 
      # with the Django 1.3 functionality
      if raw_data:
        foo = uploaded.read( 1024 )
        while foo:
          dest.write( foo )
          foo = uploaded.read( 1024 ) 
      # if not raw, it was a form upload so read in the normal Django chunks fashion
      else:
        for c in uploaded.chunks( ):
          dest.write( c )
      # got through saving the upload, report success
      return True
  except IOError:
    # could not open the file most likely
    pass
  return False