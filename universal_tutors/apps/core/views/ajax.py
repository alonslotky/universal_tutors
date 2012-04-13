from django import http
from django.conf import settings
from django.http import  HttpResponseServerError
from django.db.models import Q, Sum
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from apps.common.utils.view_utils import main_render
from apps.common.utils.date_utils import to_calendar, next_month, next_month, prev_month

import datetime

@main_render(template='core/fragments/home/_calendar.html')
def get_calendar(request, date):
    dt = date.split('-')
    date = datetime.date(int(dt[0]), int(dt[1]), 1)    
    nxt_month = next_month(date)
    prv_month = prev_month(date)
    months = [to_calendar(date), to_calendar(nxt_month)]
    
    return {
        'months': months,
        'today': datetime.date.today(),
        'next_month': nxt_month,
        'prev_month': prv_month,
    }