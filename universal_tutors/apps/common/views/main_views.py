from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.flatpages.models import FlatPage
from django.core.mail import EmailMessage

from universal_tutors.apps.common.forms import ContactForm# , FeedbackForm

from apps.common.models import *

import threading 

def server_error(request, template_name='500.html'):
    """
    500 error handler.
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL,
        'request':request
    })))

EMAIL_TOPICS = {
  'search': 'Search',
  'profiles': 'Profiles',
  'dashboard': 'Dashboard',
  'classroom': 'Classroom',
  'other': 'Other',
}

def _send_contact_email(data):
    try:
        template = loader.get_template('common/emails/new_message.html')
        context = Context({
            'data': data,
            'PROJECT_SITE_DOMAIN': settings.PROJECT_SITE_DOMAIN,
            'topic': EMAIL_TOPICS.get(data.get('topic')),
        })
        html = template.render(context)
    
        to_email = settings.CONTACT_EMAIL
        msg = EmailMessage(
                           'New Contact Message', 
                           html, 
                           data.get('email'), 
                           [to_email])
        msg.content_subtype = 'html'
        t = threading.Thread(target=msg.send, kwargs={'fail_silently': True})
        t.setDaemon(True)
        t.start()
        return True
    except:
        return False
    
    
def _save_feedback(post, questions):
    for question in questions:
        FeedbackAnswer.objects.create(
              question=question,
              option=question.feedbackquestionoption_set.get(id=int(post.get('question-%s' % question.id))),
              comment=post.get('comment-%s' % question.id)
        )

def contact_us(request):
    # flatpage = FlatPage.objects.get(url='/contact-us/')
    sent = False
    success = False
    contact = False
    feedback = False
    
    questions = FeedbackQuestion.objects.all()
    
    if request.POST:
        if request.POST.get('contact-submit', None):
            contact_form = ContactForm(request.POST, prefix='contact')
            if contact_form.is_valid():
                sent = True
                contact = True
                if _send_contact_email(contact_form.cleaned_data):
                    success = True
                else:
                    success = False
            #feedback_form = FeedbackForm(prefix='feedback')
        else:
            contact_form = ContactForm(prefix='contact')
            _save_feedback(request.POST, questions)
            sent = True
            feedback = True
#            feedback_form = FeedbackForm(request.POST, prefix='feedback')
#            if feedback_form.is_valid():
#                feedback_form.save()
#                sent = True
#                feedback = True
    else:
        contact_form = ContactForm(prefix='contact')
        # feedback_form = FeedbackForm(prefix='feedback')

    return render_to_response('common/contact_us.html', {
         'contact_form': contact_form,
         'questions': questions,
         #'feedback_form': feedback_form,
         # 'flatpage': flatpage,
         'sent': sent,
         'success': success,
         'contact': contact,
         'feedback': feedback,
     }, RequestContext(request))