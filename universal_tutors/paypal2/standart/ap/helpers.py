from django.conf import settings
from django.core.urlresolvers import reverse

from models import MassPayment, MassPaymentReceiver
from conf import *

import datetime, httplib2, urllib, httplib
from urllib import urlencode
import urlparse
from ordereddict import OrderedDict

def mass_payment(options):
    url = MASSPAYMENT_POSTBACK_ENDPOINT if not settings.PAYPAL_TEST else MASSPAYMENT_SANDBOX_POSTBACK_ENDPOINT
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


def adaptive_payment(options):
    today = datetime.date.today()

    headers = {
                'Content-type':'application/x-www-form-urlencoded',
                'Accept':'text/plain',
                'X-PAYPAL-SECURITY-USERID': settings.PAYPAL_API_USERNAME, 
                'X-PAYPAL-SECURITY-PASSWORD': settings.PAYPAL_API_PASSWORD, 
                'X-PAYPAL-SECURITY-SIGNATURE': settings.PAYPAL_API_SIGNATURE,
                'X-PAYPAL-APPLICATION-ID': settings.PAYPAL_API_APPLICATION_ID,
                'X-PAYPAL-REQUEST-DATA-FORMAT':'NV',
                'X-PAYPAL-RESPONSE-DATA-FORMAT':'NV'
                }
    
    params = {
        'actionType': 'PAY',
        'senderEmail': settings.PAYPAL_RECEIVER_EMAIL,

        'returnUrl': 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, reverse('home')),
        'cancelUrl': 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, reverse('home')),
        'ipnNotificationUrl': 'http://%s%s' % (settings.PROJECT_SITE_DOMAIN, reverse('paypal-ipn')),
        
        'startingDate': today,
        'endingDate': today + datetime.timedelta(days=1),
        
        'options': OrderedDict({'displayOptions.businessName': settings.PROJECT_NAME}),
        'requestEnvelope.detailLevel': 'ReturnAll',
        'requestEnvelope.errorLanguage': 'en_US',
        'feesPayer': 'EACHRECEIVER',
    }
    
    params.update(options)
    
    ### PAY 
    enc_params = urllib.urlencode(params)
     
    conn = httplib.HTTPSConnection(SANDBOX_SVCS_ENDPOINT if settings.DEBUG else SVCS_ENDPOINT)
    conn.request("POST", "/AdaptivePayments/Pay", enc_params, headers)
     
    response = conn.getresponse()
    data = urlparse.parse_qs(response.read())
    
    paykey = data.get('payKey', [None])[0]     
    conn.close()
    
    return {
        'paykey': paykey,
    }