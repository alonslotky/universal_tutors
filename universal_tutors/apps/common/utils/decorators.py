from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.core.serializers import json, serialize
from django.db.models import signals as signalmodule
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson
from django import template
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

from apps.profile.models import UserProfile

register = template.Library()

try:
    from functools import wraps
except ImportError: 
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner

def render_to(template=None, mimetype="text/html"):
    """
    Decorator for Django views that sends returned dict to render_to_response 
    function.

    Template name can be decorator parameter or TEMPLATE item in returned 
    dictionary.  RequestContext always added as context instance.
    If view doesn't return dict then decorator simply returns output.

    Parameters:
     - template: template name to use
     - mimetype: content type to send in response headers

    Examples:
    # 1. Template name in decorator parameters

    @render_to('template.html')
    def foo(request):
        bar = Bar.object.all()  
        return {'bar': bar}


    # 2. Template name as TEMPLATE item value in return dictionary.
         if TEMPLATE is given then its value will have higher priority 
         than render_to argument.

    @render_to()
    def foo(request, category):
        template_name = '%s.html' % category
        return {'bar': bar, 'TEMPLATE': template_name}

    """
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            return render_to_response(tmpl, output, \
                        context_instance=RequestContext(request), mimetype=mimetype)
        return wrapper
    return renderer

def register_render_tag(register):
    """
    Decorator that creates a template tag using the given renderer as the
    render function for the template tag node - the render function takes two
    arguments - the template context and the tag token
    
    Usage:
    
    @register_render_tag
    def my_tag(context, token):
        # parse the token and modify the context
        return "" 
        
    """
    
    def wrapper(renderer):
        def tag(parser, token):
            class TagNode(template.Node):
                def render(self, context):
                    return renderer(context, token)
            return TagNode()
        for copy_attr in ("__dict__", "__doc__", "__name__"):
            setattr(tag, copy_attr, getattr(renderer, copy_attr))
        return register.tag(tag)
    return wrapper


def type_required(type_required_url = None):
    """
    Decorator that force a authenticated user have a type
    
    Usage:
    
    @type_required('type_required_url')
    def my_view(request):
        # any action
        return "" 
        
    """
    
    return user_passes_test(
        lambda u: u.is_authenticated() and u.profile.type != UserProfile.TYPES.NONE,
        login_url = type_required_url or settings.TYPE_URL
    )


def over16_required(under16_url = None):
    """
    Decorator that force a authenticated user being over16
    
    Usage:
    
    @over16_required('under16_url')
    def my_view(request):
        # any action
        return "" 
        
    """
    
    return user_passes_test(
        lambda u: u.is_authenticated() and u.profile.type != UserProfile.TYPES.NONE and u.profile.type != UserProfile.TYPES.UNDER16,
        login_url = under16_url or settings.UNDER16_URL
    )
