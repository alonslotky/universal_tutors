from django import http
from django.conf import settings
from django.http import  HttpResponseServerError
from django.db.models import Q, Sum
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from apps.common.utils.view_utils import main_render

import datetime

@main_render(template='core/home.html')
def home(request):
    user = request.user

    return {}

@main_render(template='core/search.html')
def search(request):
    today = datetime.date.today()

    # get values and protected from injected values
    date, location, center, type, ordering, radius = get_searching_values(request)

    nxt_month = next_month(date)
    prv_month = prev_month(date)
    months = [to_calendar(date), to_calendar(nxt_month)]

    spaces = search_spaces(center, radius)

    context = {
        'home': True,
        'spaces': spaces,

        'months': months,
        'today': today,
        'next_month': nxt_month,
        'prev_month': prv_month,

        'location': location,
        'ordering': ordering,
        'type': type,
        'date': date,
        'radius': radius,
        'center': center,
    }
    context.update(get_defaults_space())
    return context
