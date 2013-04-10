import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from apps.core.models import Currency
from apps.profile.models import Tutor, WithdrawItem, Message

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
