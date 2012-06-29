from django import http
from django.conf import settings
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from apps.common.utils.view_utils import main_render
from apps.faq.models import *

from itertools import chain


@main_render(template='faq/faq.html')
def faq(request):
    user = request.user

    return {
        'faqs': list(chain(FAQItem.objects.filter(section__isnull=True), FAQItem.objects.filter(section__isnull=False)))
    }
