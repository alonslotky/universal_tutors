from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.template import Context

import threading, sys, traceback

# ------------------------------
# GENERIC
# ------------------------------
def formatExceptionInfo(maxTBlevel=5):
     cla, exc, trbk = sys.exc_info()
     excName = cla.__name__
     try:
         excArgs = exc.__dict__["args"]
     except KeyError:
         excArgs = "<no args>"
     excTb = traceback.format_tb(trbk, maxTBlevel)
     return (excName, excArgs, excTb)

# ------------------------------
# EMAIL
# ------------------------------
def create_email(subject, body, recipients, bcc, attachment=None, attachment_content_type=None, content_subtype="html"):
    msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, bcc)
    
    if attachment:
        msg.attach(attachment.name, attachment.read(), attachment_content_type)
    
    if content_subtype:
        msg.content_subtype = content_subtype
    return msg
    
def send_threaded_email(msg, **kwargs):
    msg.send()
    
def create_threaded_email(request, subject, body, recipients, attachment=None, attachment_content_type=None):
    msg = create_email(subject, body, recipients, [], attachment=None, attachment_content_type=None)
    
    t = threading.Thread(target=send_threaded_email,
                         args=[msg],
                         kwargs={'fail_silently': True})
    t.setDaemon(True)
    t.start()
    
def send_email(subject, body, recipients, bcc, attachment=None, attachment_content_type=None):
    msg = create_email(subject, body, recipients, bcc, attachment=None, attachment_content_type=None)
    msg.send()
    
def send_templated_email(template, ctx_dict, subject, recipients, bcc, attachment=None, attachment_content_type=None, content_subtype="html"):
    site = Site.objects.get_current()
    body = render_to_string(template, Context(dict(ctx_dict, site=site)))
    
    msg = create_email(subject, body, recipients, bcc, attachment=None, attachment_content_type=None, content_subtype=content_subtype)
    msg.send()