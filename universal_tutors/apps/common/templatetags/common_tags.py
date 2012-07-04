from django import template
from django.core.paginator import Paginator, InvalidPage
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.functional import allow_lazy
from django.template.defaultfilters import stringfilter
from django.conf import settings
from django.utils.encoding import force_unicode
from apps.common.utils.date_utils import convert_datetime as convert_datetime_

from allauth.facebook.models import FacebookApp

import datetime
import pytz

from HTMLParser import HTMLParser, HTMLParseError
    
register = template.Library()

@register.filter
def range_to(begin, end):
    return range(begin, end)

@register.filter
def slice_list(list, no_items):
    return list[:no_items]

@register.filter
def multiply(x, y):
    return x*y

@register.filter
def paragraphs(var, arg):
    """ Retrieves n number of paragraphs from the supplied text. It doesn't remove 
    any existing tags inside paragraphs."""
    class ParagraphParser(HTMLParser):
        def __init__(self, *args, **kwargs):
            HTMLParser.__init__(self)
            self.stack = []
            self.paragraphs = int(arg)
            self.in_p = False
            self.p_count = 0
            
        def handle_starttag(self, tag, attrs):   
            if tag == 'p' or tag == 'h2' or tag == 'table':
                if self.p_count < self.paragraphs:
                    self.in_p = True
                    self.p_count += 1
                else:
                    self.in_p = False
            
            if self.in_p:
                self.stack.append(self.__html_start_tag(tag, attrs))


        def handle_endtag(self, tag):
            if self.in_p:
                self.stack.append(u"</%s>" % (tag))
                if tag == 'p' or tag == 'h2' or tag == 'table':
                    self.in_p = False
        
        def handle_startendtag(self, tag, attrs):
            if self.in_p:
                self.stack.append(self.__html_startend_tag(tag, attrs))

        def handle_data(self, data):
            if self.in_p:
                self.stack.append(data)

        def __html_attrs(self, attrs):
            _attrs = u""
            try:
                _attrs = u" %s" % (' '.join([('%s="%s"' % (k,v)) for k,v in attrs.iteritems()]))
            except:
                _attrs = u" %s" % (' '.join([('%s="%s"' % (k,v)) for k,v in attrs]))
            return _attrs

        def __html_start_tag(self, tag, attrs):
            return u"<%s%s>" % (tag, self.__html_attrs(attrs)) 
        
        def __html_startend_tag(self, tag, attrs):
            return "<%s%s/>" % (tag, self.__html_attrs(attrs))

        def render(self):
            return u"".join(self.stack)

    parseme = ParagraphParser()
    
    try:
        parseme.feed(var)
    except HTMLParseError:
        return var
    
    return parseme.render()

# make sure output is not escaped... it contains HTML!
paragraphs.is_safe = True

@register.filter
def paragraphs_ignore(var, arg):
    """ Retrieves n number of paragraphs from the supplied text. It doesn't remove 
    any existing tags inside paragraphs."""
    class ParagraphParser(HTMLParser):
        def __init__(self, *args, **kwargs):
            HTMLParser.__init__(self)
            self.stack = []
            self.paragraphs = int(arg)
            self.in_p = False
            self.p_count = 0
            
        def handle_starttag(self, tag, attrs):   
            if tag == 'p' or tag == 'h2' or tag == 'table':
                if self.p_count >= self.paragraphs:
                    self.in_p = True
                else:
                    self.in_p = False
                    self.p_count += 1
            
            if self.in_p:
                self.stack.append(self.__html_start_tag(tag, attrs))


        def handle_endtag(self, tag):
            if self.in_p:
                self.stack.append(u"</%s>" % (tag))
                if tag == 'p' or tag == 'h2' or tag == 'table':
                    self.in_p = False
        
        def handle_startendtag(self, tag, attrs):
            if self.in_p:
                self.stack.append(self.__html_startend_tag(tag, attrs))

        def handle_data(self, data):
            if self.in_p:
                self.stack.append(data)

        def __html_attrs(self, attrs):
            _attrs = u""
            if attrs:
                try:
                    _attrs = u" %s" % (' '.join([('%s="%s"' % (k,v)) for k,v in attrs.iteritems()]))
                except:
                    _attrs = u" %s" % (' '.join([('%s="%s"' % (k,v)) for k,v in attrs]))
            return _attrs

        def __html_start_tag(self, tag, attrs):
            return u"<%s%s>" % (tag, self.__html_attrs(attrs)) 
        
        def __html_startend_tag(self, tag, attrs):
            return "<%s%s/>" % (tag, self.__html_attrs(attrs))

        def render(self):
            return u"".join(self.stack)

    parseme = ParagraphParser()
    
    try:
        parseme.feed(var)
    except HTMLParseError:
        return var
    
    return parseme.render()

# make sure output is not escaped... it contains HTML!
paragraphs_ignore.is_safe = True

class ContentHolderNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        body = self.nodelist.render(context)
        
        returnString = '''
        <div class="container">
        	<div class="container-t">
        		<div class="container-b">
        		    %s
        		</div>
        	</div>
        </div>
        ''' % (body)
        return returnString

@register.tag
def contentholder(parser, token):
    """
    Places everything between ``{% contentholder %}`` and ``{% endcontentholder %}`` into a callout box.
    """
    nodelist = parser.parse(('endcontentholder',))
    parser.delete_first_token()
    
    bits = token.split_contents()
    
    return ContentHolderNode(nodelist)

@register.inclusion_tag('common/shared_pluggables/tabs/tab_manager.html')
def create_tabs(tabs):
    tab_data = tabs["tab_data"]
    tab_url_params = "&".join(['%s=%s' % (key, value) for key, value in tabs["tab_url_params"]])
    if tab_url_params:
        tab_url_params = "?%s" % tab_url_params
    return {'tab_data': tab_data, 'tab_url_params':tab_url_params}
    
@register.inclusion_tag('common/shared_pluggables/social/social_sharing.html')
def social_share():
    return {'share_this_id': settings.SHARE_THIS_ID}
    
@register.inclusion_tag('common/view_helpers/render_generic_view.html')
def render_ajax_view(view_name):
    """
    Renders a view to a template, but loads it via AJAX
    Example {% render_ajax_view 'appname__viewname' %}
    """
    return {'view_name': view_name}
    
@register.filter
def random_test_image_if_none(img):
    """
    Returns a random test image if the image object is none and we're in debug mode
    """
    if not img and settings.DEBUG:
        return "http://placehold.it/350x150"
    else:
        return img


"""
    STRING MANIPULATION AND COMPARISON METHODS
"""
@register.filter
def contains(value, arg):
	"""
	Usage: {% if link_url|contains:"http://www.youtube.com/" %}...
	"""
	return arg in str(value)
	
def truncate_chars(s, num):
    """
    Template filter to truncate a string to at most num characters respecting word
    boundaries.
    """
    s = force_unicode(s)
    length = int(num)
    if len(s) > length:
        length = length - 3
        if s[length-1] == ' ' or s[length] == ' ':
            s = s[:length].strip()
        else:
            words = s[:length].split()
            if len(words) > 1:
                del words[-1]
            s = u' '.join(words)
        s += '...'
    return s
truncate_chars = allow_lazy(truncate_chars, unicode)

@register.filter
@stringfilter
def truncatechars(value, arg):
    """
    Truncates a string after a certain number of characters, but respects word boundaries.
    
    Argument: Number of characters to truncate after.
    """
    try:
        length = int(arg)
    except ValueError: # If the argument is not a valid integer.
        return value # Fail silently.
    return truncate_chars(value, length)
truncatechars.is_safe = True


"""
    IMAGE HELPER METHODS
"""
@register.simple_tag
def thumbnail(image_url, width, height):
    """
    Given the url to an image, resizes the image using the given width and 
    height on the first time it is requested, and returns the url to the new 
    resized image. If width or height are zero then the original ratio is 
    maintained.
    """
    
    image_url = unicode(image_url)
    image_path = os.path.join(settings.MEDIA_ROOT, image_url)
    image_dir, image_name = os.path.split(image_path)
    thumb_name = "%s-%sx%s.jpg" % (os.path.splitext(image_name)[0], width, height)
    thumb_path = os.path.join(image_dir, thumb_name)
    thumb_url = "%s/%s" % (os.path.dirname(image_url), thumb_name)

    # abort if thumbnail exists, original image doesn't exist, invalid width or 
    # height are given, or PIL not installed
    if not image_url:
        return ""
    if os.path.exists(thumb_path):
        return thumb_url
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        return image_url
    if not os.path.exists(image_path) or (width == 0 and height == 0):
        return image_url
    try:
        from PIL import Image, ImageOps
    except ImportError:
        return image_url

    # open image, determine ratio if required and resize/crop/save
    image = Image.open(image_path)
    if width == 0:
        width = image.size[0] * height / image.size[1]
    elif height == 0:
        height = image.size[1] * width / image.size[0]
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
    try:
        image = ImageOps.fit(image, (width, height), Image.ANTIALIAS).save(
            thumb_path, "JPEG", quality=100)
    except:
        return image_url
    return thumb_url
    
@register.inclusion_tag('ui/buttons/delete.html')
def delete_button(name, value):
    return {
    'name': name,
    'value': value,
    }


@register.inclusion_tag('ui/buttons/submit.html')
def submit_button(name, value):
    return {
    'name': name,
    'value': value,
    }


@register.inclusion_tag('ui/buttons/button.html')
def button(name, value, id):
    if not id:
        id = "id_%s" % name

    return {
    'name': name,
    'value': value,
    'id': id,
    }

@register.filter
def age(date):
    if date:
        today = datetime.date.today()
        years = today.year - date.year
        if date.month > today.month:
            years -= 1
        elif date.month == today.month:
            if date.day > today.day:
                years -= 1
                
        return years
    else:
        return '--'

@register.filter
def convert_datetime(dt, timezone):
    return convert_datetime_(dt, pytz.utc, timezone) if dt else ''


@register.filter
def sub(x, y):
    return x-y

@register.filter
def customnaturalday(value):
    """
    For date and time values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    try:
        now = datetime.datetime.now()
        value = datetime.date(value.year, value.month, value.day)
    except AttributeError:
        return value
    except ValueError:
        return value

    today = datetime.date.today()
    time = ''

    if value == today:
        return 'Today'

    elif value < today:
        delta = today - value
        if delta.days == 1:
            return 'Yesterday'
        if delta.days < 8:
            return "%s days ago" % delta.days
        if delta.days < 30:
            value = delta.days // 7
            return "%s %s ago" % (value, 'weeks' if value != 1 else 'week')
        if delta.days < 355:
            value = delta.days // 30
            return "%s %s ago" % (value, 'months' if value != 1 else 'month')
        
        value = delta.days // 355
        return "%s %s ago" (value, 'years' if value != 1 else 'year')

    else:
        delta = value - today
        if delta.days == 1:
            return 'Tomorrow'
        if delta.days < 8:
            return "%s days from today" % delta.days
        if delta.days < 30:
            value = delta.days // 7
            return "%s %s from today" % (value, 'weeks' if value != 1 else 'week')
        if delta.days < 355:
            value = delta.days // 30
            return "%s %s from now" % (value, 'months' if value != 1 else 'month')

        value = delta.days // 355
        return "%s %s from now" (value, 'years' if value != 1 else 'year')

@register.filter
def customnaturaltime(value):
    """
    For date and time values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    try:
        value = datetime.datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)
    except AttributeError:
        return value
    except ValueError:
        return value

    if getattr(value, 'tzinfo', None):
        now = datetime.datetime.now(LocalTimezone(value))
    else:
        now = datetime.datetime.now()
    now = now - datetime.timedelta(0, 0, now.microsecond)

    time = ''

    if value < now:
        delta = now - value
        #if delta.days != 0:
        #    return "%s ago" % defaultfilters.timesince(value)
        years = delta.days / 365
        weeks = delta.days / 7
        months = weeks / 4
        if years != 0:
            return '%d years ago' % years if years > 1 else 'a year ago'
        elif months != 0:
            return '%d months ago' % months if months > 1 else 'a month ago'
        elif delta.days != 0:
            return '%s days ago' % delta.days if delta.days > 1 else 'a day ago'
        elif delta.seconds == 0:
            return 'now'
        elif delta.seconds < 60:
            return '%s seconds ago' % delta.seconds if delta.seconds > 1 else 'a second ago'
        elif delta.seconds / 60 < 60:
            count = delta.seconds / 60
            return '%s minutes ago' % count if count > 1 else 'a minute ago'
        else:
            count = delta.seconds / 60 / 60
            return '%s hours ago' % count if count > 1 else 'an hour ago'
    else:
        delta = value - now
        #if delta.days != 0:
        #    return '%s from now' % defaultfilters.timeuntil(value)
        years = delta.days / 365
        weeks = delta.days / 7
        months = weeks / 4
        if years != 0:
            return '%d years ago' % years if years > 1 else 'a year from now'
        elif months != 0:
            return '%d months ago' % months if months > 1 else 'a month from now'
        elif delta.days != 0:
            return '%s days ago' % delta.days if delta.days > 1 else 'a day from now'
        elif delta.seconds == 0:
            return 'now'
        elif delta.seconds < 60:
            return '%s seconds from now' % delta.seconds if delta.seconds > 1 else 'a second from now'
        elif delta.seconds / 60 < 60:
            count = delta.seconds / 60
            return '%(count)s minutes from now' % count if count > 1 else 'a minute from now'
        else:
            count = delta.seconds / 60 / 60
            return '%(count)s hours from now' % count if count > 1 else 'a hour from now'


@register.simple_tag
def get_facebook_api_id():
    try:
        return FacebookApp.objects.latest('id').api_key
    except FacebookApp.DoesNotExit:
        return ''