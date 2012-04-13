from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.core.urlresolvers import get_mod_func
from django.conf import settings
from django.utils.functional import Promise
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.common.utils.decorators import render_to

import simplejson
import unicodedata

"""
    View decorators and utils to assist in the view architecture we have in use here. You shouldn't need to amend anything here.
"""

class JSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            return super(JSONEncoder, self).default(o)

class JSONResponse(HttpResponse):
    def __init__(self, data):
        HttpResponse.__init__(
            self, content=simplejson.dumps(data, cls=JSONEncoder),
            #mimetype="text/html",
        )

def main_render(template=None, mimetype="text/html"):
    def wrapper(func):
        @render_to(template=template, mimetype=mimetype)
        def inner(request, *args, **kwargs):
            ret = func(request, *args, **kwargs)
            context_vars = ret
            return context_vars
        return inner
    return wrapper
    
def fragment_render():
    def wrapper(func):
        def inner(request, *args, **kwargs):
            di = func(request, *args, **kwargs)
            di['key'] = func.func_name
            c = RequestContext(request, di)
            
            template=di['template']
            return get_template(template).render(c)
        inner.name = getattr(func, 'name', func.func_name)
        return inner
    return wrapper
    
class AjaxRegistry(object):
    _instance = None
    _registry = {}
    _prefix = ""
    
    def __new__(cls, *args, **kwargs):
        if cls != type(cls._instance):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
        
    def set_prefix(self, prefix):
        self._prefix = prefix
    
    def register(self, func):
        key = "%s__%s" % (self._prefix, func.func_name)
        def wrap(*args, **kwargs):
            return func(*args, **kwargs)
        
        self._registry[key] = wrap
        wrap.key=key
        wrap.name = func.func_name
        return wrap
    
def ajax_view(request, view_name):
    if request.is_ajax() or request.method == 'POST':
        return_type = "template"
        
        if request.GET:
            if "return_type" in request.GET:
                return_type = request.GET['return_type'] 
        
        ar = AjaxRegistry()
        func = ar._registry[view_name]
        ret = func(request)
        ret['key'] = view_name
        
        if not "template" in ret:
            return_type = "json"
        
        if return_type == "template":
            return HttpResponse(get_template(ret['template']).render(RequestContext(request, ret)))
        else:
            json = simplejson.dumps(ret)
            return HttpResponse(json, mimetype='application/javascript')
    else:
        return HttpResponseNotFound()
        
def process_form(request, form_class, instance=None, is_ajax=False, commit=True, trigger_save=True, prefix=None):
    validate_only = request.REQUEST.get("validate_only") == "true"
    form = form_class(request, request.POST, request.FILES, instance=instance, prefix=prefix)
    if form.is_valid():
        if validate_only:
            return form, None, None, HttpResponse(simplejson.dumps({"valid": True, "errors": {}}), mimetype='application/javascript')
        if trigger_save:
            form_object, msg = form.save(commit=commit)
            messages.add_message(request, messages.INFO, msg)
        else:
            form_object = form
            msg = None
        if "next" in request.POST:
            return form, form_object, msg, HttpResponseRedirect(request.POST['next'])
        else:
            return form, form_object, msg, None
    else:
        if validate_only:
            if "field" in request.REQUEST:
                errors = form.errors.get(request.REQUEST["field"], "")
                if errors: errors = "".join(errors)
            else:
                errors = form.errors
            return form, None, None, HttpResponse(simplejson.dumps({ "errors": errors, "valid": not errors}), mimetype='application/javascript')
        elif is_ajax:
            result = {
                'error': True if form.errors else False,
                'errors': dict(form.errors),
                'response': "",
            }
            return form, None, None, HttpResponse(simplejson.dumps(result))
        msg = "Oops, it looks like you missed something. Please read below for the exact errors"
    messages.add_message(request, messages.INFO, msg)
    return form, None, msg, None


def easy_paginator(request, objects_list, items_per_page):
    """Return Paginator and Page instances"""
    if hasattr(objects_list,'len'):
        pg = Paginator(objects_list, items_per_page)
    else:
        pg = Paginator(list(objects_list), items_per_page)
    
    try:
        data = pg.page(request.GET.get('page', None) or \
                     request.POST.get('page', None) or 1)
    except EmptyPage, PageNotAnInteger:
	data = []

    return pg, data


def handle_uploaded_file(f, folder):
    new_filename = unicodedata.normalize('NFKD', f.name.replace(';','__').replace(',','__').replace(' ','_')).encode('ascii', 'ignore')
    destination = open('%s/%s/%s' % (settings.MEDIA_ROOT, folder, new_filename), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    return (destination, new_filename)
