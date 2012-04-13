from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.template import loader, Context

from apps.common.utils.view_utils import main_render
from apps.common.forms import ContactForm

@login_required
@main_render('common/iframes/contact.html')
def contact(request):

    form = ContactForm(request.POST or None)
    success = False
    error_message = ''

    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        body = """
        %s(%s) name has sent you a new message. The content is below:\n
        %s
        """ % (name, email, message)
        try:
            success = True
            context = Context({
                'name': name,
                'email': email,
                'message': message
             })

            t = loader.get_template('common/emails/new_message.html')
            html = t.render(context)

            subject = '[Youcoca.com] New Message from %s' % name

            msg = EmailMessage(subject, html,
                               settings.DEFAULT_FROM_EMAIL, to=list(settings.ADMINS))
            msg.content_subtype = "html"

            msg.send()

            # send_mail('New Message From %s' % name, body, email, list(settings.ADMINS), fail_silently=False)
        except:
            success = False
            error_message = 'An error occured while sending your message. Please try again in a few moments.'

    return {
        'success': success,
        'form': form,
        'error_message': error_message,
    }
