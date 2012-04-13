from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.base import ModelBase
from django.utils.safestring import mark_safe
from django.template.defaultfilters import yesno, linebreaksbr, urlize
from django.utils.translation import get_date_formats
from django.utils.text import capfirst
from django.utils import dateformat
from django.template.defaultfilters import slugify
import datetime, re, logging

try:
    from collections import namedtuple
except ImportError:
    # Python 2.4, 2.5 backport:
    # http://code.activestate.com/recipes/500261/
    from apps.common.utils.namedtuple import namedtuple

def get_namedtuple_choices(name, choices_tuple):
    """Factory function for quickly making a namedtuple suitable for use in a
    Django model as a choices attribute on a field. It will preserve order.

    Usage::

        class MyModel(models.Model):
            COLORS = get_namedtuple_choices('COLORS', (
                (0, 'BLACK', 'Black'),
                (1, 'WHITE', 'White'),
            ))
            colors = models.PositiveIntegerField(choices=COLORS)

        >>> MyModel.COLORS.BLACK
        0
        >>> MyModel.COLORS.get_choices()
        [(0, 'Black'), (1, 'White')]
    """
    class Choices(namedtuple(name, [name for val,name,desc in choices_tuple])):
        __slots__ = ()
        _choices = tuple([desc for val,name,desc in choices_tuple])

        def get_choices(self):
            return zip(tuple(self), self._choices)

    return Choices._make([val for val,name,desc in choices_tuple])

def unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
    """
    Calculates a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug. Chop its length down if we need to.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create a queryset, excluding the current instance.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '-%s' % next
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1
    
    setattr(instance, slug_field.attname, slug)

def _slug_strip(value, separator=None):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
        value = re.sub('%s+' % re_sep, separator, value)
    return re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None		

class ModelInfo(object):
    class _Meta:
        model = None
        label_width = 120
        fields = ()
        exclude = ()
        sections = None
        row_template = '<div style="height: 20px;"><div style="float:left; width: %spx; text-align: left; font-weight: bold;">%s: </div><div style="text-align: left; float: left;">%s</div></div><div class="clearer"></div>'
        show_if_none = False
        auto_urlize = True
        auto_linebreaks = True

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance

        self._meta = self.Meta()
        _meta = self._Meta()

        for attr in ('model','label_width','fields','exclude','sections','row_template','show_if_none',
                'auto_urlize','auto_linebreaks',):
            if not hasattr(self._meta, attr):
                setattr(self._meta, attr, getattr(_meta, attr))

    def get_model_fields(self):
        return [f.name for f in self._meta.model._meta.fields \
                if f.name != 'id' and \
                (f.name in self._meta.fields or \
                not f.name in self._meta.exclude)\
                ]

    def get_field(self, f_name):
        try:
            return [f for f in self._meta.model._meta.fields if f.name == f_name][0]
        except:
            pass

    def get_field_display_text(self, f_name):
        return self.get_field(f_name).verbose_name

    def get_field_display_value(self, f_name):
        field = self.get_field(f_name)

        try:
            return getattr(self, 'get_%s_value'%f_name)
        except:
            pass

        f_value = getattr(self.instance, f_name)

        if f_value is None:
            return None

        if callable(f_value):
            return f_value()
        
        if isinstance(f_value, models.Model):
            if self._meta.auto_urlize and hasattr(f_value, 'get_absolute_url'):
                return '<a href="%s">%s</a>'%(f_value.get_absolute_url(), f_value)
            else:
                return unicode(f_value)

        if field.choices:
            return dict(field.choices).get(f_value, None)

        if isinstance(field, models.BooleanField):
            return yesno(f_value)

        date_format, datetime_format, time_format = get_date_formats()

        if isinstance(field, models.DateTimeField):
            return capfirst(dateformat.format(f_value, datetime_format))

        if isinstance(field, models.TimeField):
            return capfirst(dateformat.time_format(f_value, time_format))

        if isinstance(field, models.DateField):
            return capfirst(dateformat.format(f_value, date_format))

        if isinstance(field, models.TextField):
            if self._meta.auto_urlize: f_value = urlize(f_value)
            if self._meta.auto_linebreaks: f_value = linebreaksbr(f_value)

        return f_value

    def as_string(self):
        ret = []

        sections = self._meta.sections or ((None, self._meta.fields or self.get_model_fields()),)

        for s_name, s_fields in sections:
            if s_name:
                ret.append('<div style="text-align: left; margin-top: 20px;"><h3>%s</h3></div>'%s_name)
                
            for f_name in s_fields:
                f_display = self.get_field_display_text(f_name)
                f_display = f_display[0] == f_display[0].lower() and f_display.capitalize() or f_display

                f_value = self.get_field_display_value(f_name)

                if self._meta.show_if_none or f_value is not None:
                    ret.append(self._meta.row_template%(str(self._meta.label_width), f_display, f_value))

        return mark_safe('\n'.join(ret))

    def __unicode__(self):
        return self.as_string()