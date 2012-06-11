from django.conf import settings
from models import MassPayment, MassPaymentReceiver
from conf import *

import datetime, httplib2
from urllib import urlencode

def pay(options):
    url = POSTBACK_ENDPOINT if not settings.PAYPAL_TEST else SANDBOX_POSTBACK_ENDPOINT
    data = {
        'METHOD': 'MassPay',
        'VERSION': '51.0',
        'PWD': settings.PAYPAL_API_PASSWORD, 
        'USER': settings.PAYPAL_API_USERNAME, 
        'SIGNATURE': settings.PAYPAL_API_SIGNATURE,         
        'currencyCode': options['currencyCode'],
        'receiverType': 'EmailAddress',
        'notify_url': options['notify_url'],
    }
    
    payment = MassPayment.objects.create(
        sender_email = settings.PAYPAL_RECEIVER_EMAIL,
        currency_code = options['currencyCode'],
        memo = 'Payment on %s' % datetime.datetime.now(),
    )
    
    
    for index, receiver in enumerate(options['receivers']):
        payment.receivers.create(
            email = receiver['email'],
            amount = receiver['amount'],
        )
        
        data['L_EMAIL%s' % index] = receiver['email']
        data['L_AMT%s' % index] = receiver['amount']
        data['L_UNIQUEID%s' % index] = receiver['unique_id']
    
    http = httplib2.Http()
    response, content = http.request(url, 'POST', urlencode(data))

    print '\n%s\n%s\n\n' % (data, content)
    