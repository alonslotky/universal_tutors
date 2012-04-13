from django.utils.translation import ugettext as _
from django.db import models, connection
from django.utils.text import capfirst
from itertools import chain
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode, smart_unicode
from django import forms
from itertools import chain
from django.conf import settings
from django.contrib.admin import widgets
from django.utils.html import escape
from django.forms.fields import EMPTY_VALUES, Field
from django.forms import ValidationError
from django.db.models.signals import post_delete, post_save
from south.modelsinspector import add_introspection_rules
from django.db.models import OneToOneField
from django.db.models.fields.related import SingleRelatedObjectDescriptor

qn = connection.ops.quote_name

import re

from apps.common.utils.form_fields import MultiSelectFormField
from apps.common.utils.widgets import CustomCheckboxSelectMultiple

uk_landline_re = re.compile(r'^[0]{1}[1-9]{1}[0-9]{9}$')
uk_landline_no08or09_re = re.compile(r'^[0]{1}[1-7]{1}[0-9]{9}$')
uk_mobile_re = re.compile(r'^(07)[0-9]{9}')
international_number_re = re.compile(r'^[+]?([0-9]*[\.\s\-\(\)]|[0-9]+){3,24}$')

from django.db.models import OneToOneField
from django.db.models.fields.related import SingleRelatedObjectDescriptor


class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            obj = self.related.model(**{self.related.field.name: instance})
            obj.save()
            return obj


class AutoOneToOneField(OneToOneField):
    '''
    OneToOneField creates related object on first call if it doesnt exist yet.
    Use it instead of original OneToOne field.

    example:
        
        class MyProfile(models.Model):
            user = AutoOneToOneField(User, primary_key=True)
            home_page = models.URLField(max_length=255, blank=True)
            icq = models.IntegerField(max_length=255, null=True)
    '''
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        from south.modelsinspector import introspector
        field_class = OneToOneField.__module__ + "." + OneToOneField.__name__
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

class InternationalTelNumberField(Field):
    " A InternationalTelNumberField that accepts a wide variety of valid phone number patterns. "
    default_error_messages = {
        'invalid': u'The phone number is invalid. Please ensure you have entered it in the international format.',
    }

    def clean(self, value):
        super(InternationalTelNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        
        m = international_number_re.match(smart_unicode(value))
        if m:
            return u'%s' % (value)
        raise ValidationError(self.error_messages['invalid'])

class UKLandlineField(Field):
    " A UKLandlineField that accepts a wide variety of valid phone number patterns. "
    default_error_messages = {
        'invalid': u'The phone number is invalid. Please ensure you have no spaces or dashes.',
    }

    def clean(self, value):
        super(UKLandlineField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        
        m = uk_landline_re.match(smart_unicode(value))
        if m:
            return u'%s' % (value)
        raise ValidationError(self.error_messages['invalid'])
        
class UKLandlineNo08or09Field(Field):
    " A UKLandlineNo08or09Field that accepts a wide variety of valid phone number patterns. Except for those starting with 08 or 09"
    default_error_messages = {
        'invalid': u'The phone number is invalid. Please ensure you have no spaces or dashes and that the number cannot start with 08 or 09.',
    }

    def clean(self, value):
        super(UKLandlineNo08or09Field, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        
        m = uk_landline_no08or09_re.match(smart_unicode(value))
        if m:
            return u'%s' % (value)
        raise ValidationError(self.error_messages['invalid'])
        
class UKMobileField(Field):
    " A UKMobileField that accepts a wide variety of valid phone number patterns."
    default_error_messages = {
        'invalid': u'The mobile number is invalid. Please ensure you have no spaces or dashes.',
    }

    def clean(self, value):
        super(UKMobileField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        
        m = uk_mobile_re.match(smart_unicode(value))
        if m:
            return u'%s' % (value)
        raise ValidationError(self.error_messages['invalid'])

class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name), 
                    'help_text': self.help_text, 'choices':self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value:
            return value.split(",")
        else:
            return []
        
    def validate(self, value, model_instance): 
        return

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(self.choices):",".join([choicedict.get(value,value) for value in getattr(self,fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)
            
# ISO 3166-1 country names and codes adapted from http://opencountrycodes.appspot.com/python/
COUNTRIES = [
    ('UK', _('United Kingdom')),
    ('US', _('United States')),
    ('AF', _('Afghanistan')), 
    ('AX', _('Aland Islands')), 
    ('AL', _('Albania')), 
    ('DZ', _('Algeria')), 
    ('AS', _('American Samoa')), 
    ('AD', _('Andorra')), 
    ('AO', _('Angola')), 
    ('AI', _('Anguilla')), 
    ('AQ', _('Antarctica')), 
    ('AG', _('Antigua and Barbuda')), 
    ('AR', _('Argentina')), 
    ('AM', _('Armenia')), 
    ('AW', _('Aruba')), 
    ('AU', _('Australia')), 
    ('AT', _('Austria')), 
    ('AZ', _('Azerbaijan')), 
    ('BS', _('Bahamas')), 
    ('BH', _('Bahrain')), 
    ('BD', _('Bangladesh')), 
    ('BB', _('Barbados')), 
    ('BY', _('Belarus')), 
    ('BE', _('Belgium')), 
    ('BZ', _('Belize')), 
    ('BJ', _('Benin')), 
    ('BM', _('Bermuda')), 
    ('BT', _('Bhutan')), 
    ('BO', _('Bolivia')), 
    ('BA', _('Bosnia and Herzegovina')), 
    ('BW', _('Botswana')), 
    ('BV', _('Bouvet Island')), 
    ('BR', _('Brazil')), 
    ('BN', _('Brunei Darussalam')), 
    ('BG', _('Bulgaria')), 
    ('BF', _('Burkina Faso')), 
    ('BI', _('Burundi')), 
    ('KH', _('Cambodia')), 
    ('CM', _('Cameroon')), 
    ('CA', _('Canada')), 
    ('CV', _('Cape Verde')), 
    ('KY', _('Cayman Islands')), 
    ('CF', _('Central African Republic')), 
    ('TD', _('Chad')), 
    ('CL', _('Chile')), 
    ('CN', _('China')), 
    ('CX', _('Christmas Island')), 
    ('CC', _('Cocos Islands')), 
    ('CO', _('Colombia')), 
    ('KM', _('Comoros')), 
    ('CG', _('Congo')), 
    ('CD', _('Congo')), 
    ('CK', _('Cook Islands')), 
    ('CR', _('Costa Rica')), 
    ('CI', _("Cote d'Ivoire")), 
    ('HR', _('Croatia')), 
    ('CU', _('Cuba')), 
    ('CY', _('Cyprus')), 
    ('CZ', _('Czech Republic')), 
    ('DK', _('Denmark')), 
    ('DJ', _('Djibouti')), 
    ('DM', _('Dominica')), 
    ('DO', _('Dominican Republic')), 
    ('EC', _('Ecuador')), 
    ('EG', _('Egypt')), 
    ('SV', _('El Salvador')), 
    ('GQ', _('Equatorial Guinea')), 
    ('ER', _('Eritrea')), 
    ('EE', _('Estonia')), 
    ('ET', _('Ethiopia')), 
    ('FK', _('Falkland Islands')), 
    ('FO', _('Faroe Islands')), 
    ('FJ', _('Fiji')), 
    ('FI', _('Finland')), 
    ('FR', _('France')), 
    ('GF', _('French Guiana')), 
    ('PF', _('French Polynesia')), 
    ('GA', _('Gabon')), 
    ('GM', _('Gambia')), 
    ('GE', _('Georgia')), 
    ('DE', _('Germany')), 
    ('GH', _('Ghana')), 
    ('GI', _('Gibraltar')), 
    ('GR', _('Greece')), 
    ('GL', _('Greenland')), 
    ('GD', _('Grenada')), 
    ('GP', _('Guadeloupe')), 
    ('GU', _('Guam')), 
    ('GT', _('Guatemala')), 
    ('GG', _('Guernsey')), 
    ('GN', _('Guinea')), 
    ('GW', _('Guinea-Bissau')), 
    ('GY', _('Guyana')), 
    ('HT', _('Haiti')),
    ('HN', _('Honduras')), 
    ('HK', _('Hong Kong')), 
    ('HU', _('Hungary')), 
    ('IS', _('Iceland')), 
    ('IN', _('India')), 
    ('ID', _('Indonesia')), 
    ('IR', _('Iran')), 
    ('IQ', _('Iraq')), 
    ('IE', _('Ireland')), 
    ('IM', _('Isle of Man')), 
    ('IL', _('Israel')), 
    ('IT', _('Italy')), 
    ('JM', _('Jamaica')), 
    ('JP', _('Japan')), 
    ('JE', _('Jersey')), 
    ('JO', _('Jordan')), 
    ('KZ', _('Kazakhstan')), 
    ('KE', _('Kenya')), 
    ('KI', _('Kiribati')), 
    ('KP', _('Korea')), 
    ('KR', _('Korea, Republic of')), 
    ('KW', _('Kuwait')), 
    ('KG', _('Kyrgyzstan')), 
    ('LA', _('Lao')), 
    ('LV', _('Latvia')), 
    ('LB', _('Lebanon')), 
    ('LS', _('Lesotho')), 
    ('LR', _('Liberia')), 
    ('LY', _('Libyan Arab Jamahiriya')), 
    ('LI', _('Liechtenstein')), 
    ('LT', _('Lithuania')), 
    ('LU', _('Luxembourg')), 
    ('MO', _('Macao')), 
    ('MK', _('Macedonia')), 
    ('MG', _('Madagascar')), 
    ('MW', _('Malawi')), 
    ('MY', _('Malaysia')), 
    ('MV', _('Maldives')), 
    ('ML', _('Mali')), 
    ('MT', _('Malta')), 
    ('MH', _('Marshall Islands')), 
    ('MQ', _('Martinique')), 
    ('MR', _('Mauritania')), 
    ('MU', _('Mauritius')), 
    ('YT', _('Mayotte')), 
    ('MX', _('Mexico')), 
    ('MD', _('Moldova')), 
    ('MC', _('Monaco')), 
    ('MN', _('Mongolia')), 
    ('ME', _('Montenegro')), 
    ('MS', _('Montserrat')), 
    ('MA', _('Morocco')), 
    ('MZ', _('Mozambique')), 
    ('MM', _('Myanmar')), 
    ('NA', _('Namibia')), 
    ('NR', _('Nauru')), 
    ('NP', _('Nepal')), 
    ('NL', _('Netherlands')), 
    ('AN', _('Netherlands Antilles')), 
    ('NC', _('New Caledonia')), 
    ('NZ', _('New Zealand')), 
    ('NI', _('Nicaragua')), 
    ('NE', _('Niger')), 
    ('NG', _('Nigeria')), 
    ('NU', _('Niue')), 
    ('NF', _('Norfolk Island')), 
    ('MP', _('Northern Mariana Islands')), 
    ('NO', _('Norway')), 
    ('OM', _('Oman')), 
    ('PK', _('Pakistan')), 
    ('PW', _('Palau')),  
    ('PA', _('Panama')), 
    ('PG', _('Papua New Guinea')), 
    ('PY', _('Paraguay')), 
    ('PE', _('Peru')), 
    ('PH', _('Philippines')), 
    ('PN', _('Pitcairn')), 
    ('PL', _('Poland')), 
    ('PT', _('Portugal')), 
    ('PR', _('Puerto Rico')), 
    ('QA', _('Qatar')), 
    ('RE', _('Reunion')), 
    ('RO', _('Romania')), 
    ('RU', _('Russian Federation')), 
    ('RW', _('Rwanda')), 
    ('BL', _('Saint Barthelemy')), 
    ('SH', _('Saint Helena')), 
    ('KN', _('Saint Kitts and Nevis')), 
    ('LC', _('Saint Lucia')), 
    ('MF', _('Saint Martin')), 
    ('WS', _('Samoa')), 
    ('SM', _('San Marino')), 
    ('ST', _('Sao Tome and Principe')), 
    ('SA', _('Saudi Arabia')), 
    ('SN', _('Senegal')), 
    ('RS', _('Serbia')), 
    ('SC', _('Seychelles')), 
    ('SL', _('Sierra Leone')), 
    ('SG', _('Singapore')), 
    ('SK', _('Slovakia')), 
    ('SI', _('Slovenia')), 
    ('SB', _('Solomon Islands')), 
    ('SO', _('Somalia')), 
    ('ZA', _('South Africa')),  
    ('ES', _('Spain')), 
    ('LK', _('Sri Lanka')), 
    ('SD', _('Sudan')), 
    ('SR', _('Suriname')), 
    ('SJ', _('Svalbard and Jan Mayen')), 
    ('SZ', _('Swaziland')), 
    ('SE', _('Sweden')), 
    ('CH', _('Switzerland')), 
    ('SY', _('Syrian Arab Republic')), 
    ('TW', _('Taiwan')), 
    ('TJ', _('Tajikistan')), 
    ('TZ', _('Tanzania')), 
    ('TH', _('Thailand')), 
    ('TL', _('Timor-Leste')), 
    ('TG', _('Togo')), 
    ('TK', _('Tokelau')), 
    ('TO', _('Tonga')), 
    ('TT', _('Trinidad and Tobago')), 
    ('TN', _('Tunisia')), 
    ('TR', _('Turkey')), 
    ('TM', _('Turkmenistan')), 
    ('TC', _('Turks and Caicos Islands')), 
    ('TV', _('Tuvalu')), 
    ('UG', _('Uganda')), 
    ('UA', _('Ukraine')), 
    ('AE', _('United Arab Emirates')),
    ('UY', _('Uruguay')), 
    ('UZ', _('Uzbekistan')), 
    ('VU', _('Vanuatu')), 
    ('VE', _('Venezuela')), 
    ('VN', _('Viet Nam')), 
    ('VG', _('Virgin Islands, British')), 
    ('VI', _('Virgin Islands, U.S.')), 
    ('WF', _('Wallis and Futuna')), 
    ('EH', _('Western Sahara')), 
    ('YE', _('Yemen')), 
    ('ZM', _('Zambia')), 
    ('ZW', _('Zimbabwe')), 
]

class CountryField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"
        
class PositionField(models.IntegerField):
    """A model field to manage the position of an item within a collection.

    By default all instances of a model are treated as one collection; if the
    ``unique_for_field`` argument is used, each value of the specified field is
    treated as a distinct collection.

    ``PositionField`` values work like list indices, including the handling of
    negative values.  A value of ``-2`` will be cause the position to be set to
    the second to last position in the collection.  The implementation differs
    from standard list indices in that values that are too large or too small
    are converted to the maximum or minimum allowed value respectively.

    When the value of a ``PositionField`` in a model instance is modified, the
    positions of other instances in the same collection are automatically
    updated to reflect the change.

    Assigning a value of ``None`` to a ``PositionField`` will cause the instance
    to be moved to the end of the collection (or appended to the collection, in
    the case of a new instance).

    """
    def __init__(self, verbose_name=None, name=None, unique_for_field=None, *args, **kwargs):
        # blank values are used to move an instance to the last position
        kwargs.setdefault('blank', True)

        # unique constraints break the ability to execute a single query to
        # increment or decrement a set of positions; they also require the use
        # of temporary placeholder positions which result in undesirable
        # additional queries
        unique = kwargs.get('unique', False)
        if unique:
            raise TypeError(
                '%s cannot have a unique constraint' % self.__class__.__name__
            )

        super(PositionField, self).__init__(verbose_name, name, *args, **kwargs)
        self.unique_for_field = unique_for_field

    def contribute_to_class(self, cls, name):
        super(PositionField, self).contribute_to_class(cls, name)

        # use this object as the descriptor for field access
        setattr(cls, self.name, self)

        # adjust related positions in response to a delete or save
        post_delete.connect(self._on_delete, sender=cls)
        post_save.connect(self._on_save, sender=cls)

    def get_internal_type(self):
        # all values will be positive after pre_save
        return 'PositiveIntegerField'

    def pre_save(self, model_instance, add):
        current, updated = self._get_instance_cache(model_instance)

        # existing instance, position not modified; no cleanup required
        if current is not None and updated is None:
            self._reset_instance_cache(model_instance, current)
            return current

        count = self._get_instance_peers(model_instance).count()
        if current is None:
            max_position = count
        else:
            max_position = count - 1
        min_position = 0

        # new instance; appended; no cleanup required
        if current is None and (updated == -1 or updated >= max_position):
            self._reset_instance_cache(model_instance, max_position)
            return max_position

        if max_position >= updated >= min_position:
            # positive position; valid index
            position = updated
        elif updated > max_position:
            # positive position; invalid index
            position = max_position
        elif abs(updated) <= (max_position + 1):
            # negative position; valid index

            # add 1 to max_position to make this behave like a negative list
            # index.  -1 means the last position, not the last position minus 1

            position = max_position + 1 + updated
        else:
            # negative position; invalid index
            position = min_position

        # instance inserted; cleanup required on post_save
        self._set_instance_cache(model_instance, position)
        return position

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError('%s must be accessed via instance' % self.name)
        current, updated = self._get_instance_cache(instance)
        if updated is None:
            return current
        return updated

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError('%s must be accessed via instance' % self.name)
        self._set_instance_cache(instance, value)

    def _get_instance_cache(self, instance):
        try:
            current, updated = getattr(instance, self.get_cache_name())
        except (AttributeError, TypeError):
            current, updated = None, None
        return current, updated

    def _reset_instance_cache(self, instance, value):
        try:
            delattr(instance, self.get_cache_name())
        except AttributeError:
            pass
        setattr(instance, self.get_cache_name(), (value, None))

    def _set_instance_cache(self, instance, value):
        has_pk = bool(getattr(instance, instance._meta.pk.attname))

        # default to None for existing instances; -1 for new instances
        updated = None if has_pk else -1

        try:
            current = getattr(instance, self.get_cache_name())[0]
        except (AttributeError, TypeError):
            if has_pk:
                current = value
            else:
                current = None
                if value is not None:
                    updated = value
        else:
            if value is None:
                updated = -1
            elif value != current:
                updated = value

        setattr(instance, self.get_cache_name(), (current, updated))

    def _get_instance_peers(self, instance):
        # return a queryset containing all instances of the model that belong
        # to the same collection as instance; either all instances of a model
        # or all instances with the same value in unique_for_field
        filters = {}
        if self.unique_for_field:
            unique_for_field = instance._meta.get_field(self.unique_for_field)
            unique_for_value = getattr(instance, unique_for_field.attname)
            if unique_for_field.null and unique_for_value is None:
                filters['%s__isnull' % unique_for_field.name] = True
            else:
                filters[unique_for_field.name] = unique_for_value
        return instance.__class__._default_manager.filter(**filters)

    def _on_delete(self, sender, instance, **kwargs):
        current, updated = self._get_instance_cache(instance)
        
        # decrement positions gt current
        operations = [self._get_operation_sql('-')]
        conditions = [self._get_condition_sql('>', current)]

        cursor = connection.cursor()
        cursor.execute(self._get_update_sql(instance, operations, conditions))
        self._reset_instance_cache(instance, None)

    def _on_save(self, sender, instance, **kwargs):
        current, updated = self._get_instance_cache(instance)

        # no cleanup required
        if updated is None:
            return None

        if current is None:
            # increment positions gte updated
            operations = [self._get_operation_sql('+')]
            conditions = [self._get_condition_sql('>=', updated)]
        elif updated > current:
            # decrement positions gt current and lte updated
            operations = [self._get_operation_sql('-')]
            conditions = [
                self._get_condition_sql('>', current),
                self._get_condition_sql('<=', updated)
            ]
        else:
            # increment positions lt current and gte updated
            operations = [self._get_operation_sql('+')]
            conditions = [
                self._get_condition_sql('<', current),
                self._get_condition_sql('>=', updated)
            ]

        # exclude instance from the update
        conditions.append('%(pk_field)s != %(pk)s' % {
            'pk': getattr(instance, instance._meta.pk.attname),
            'pk_field': qn(instance._meta.pk.column)
        })

        cursor = connection.cursor()
        cursor.execute(self._get_update_sql(instance, operations, conditions))
        self._reset_instance_cache(instance, updated)

    def _get_update_sql(self, instance, operations=None, conditions=None):
        operations = operations or []
        conditions = conditions or []

        params = {
            'position_field': qn(self.column),
            'table': qn(instance._meta.db_table),
        }
        if self.unique_for_field:
            unique_for_field = instance._meta.get_field(self.unique_for_field)
            unique_for_value = getattr(instance, unique_for_field.attname)

            params['unique_for_field'] = qn(unique_for_field.column)

            # this field is likely to be indexed; put it first
            if unique_for_field.null and unique_for_value is None:
                conditions.insert(0, '%(unique_for_field)s IS NULL')
            else:
                params['unique_for_value'] = unique_for_value
                conditions.insert(0,
                                  '%(unique_for_field)s = %(unique_for_value)s')

        query = 'UPDATE %(table)s'
        query += ' SET %s' % ', '.join(operations)
        query += ' WHERE %s' % ' AND '.join(conditions)

        return query % params

    def _get_condition_sql(self, gt_or_lt, position):
        return '%%(position_field)s %(gt_or_lt)s %(position)s' % {
            'gt_or_lt': gt_or_lt,
            'position': position
        }

    def _get_operation_sql(self, plus_or_minus):
        return """
        %%(position_field)s = (%%(position_field)s %(plus_or_minus)s 1)""" % {
            'plus_or_minus': plus_or_minus
        }
        
# SOUTH INTROSPECTION RULES
add_introspection_rules([], ["^apps\.common\.utils\.fields\.MultiSelectField"])
add_introspection_rules([], ["^apps\.common\.utils\.fields\.PositionField"])
add_introspection_rules([], ["^filebrowser\.fields\.FileBrowseField"])
add_introspection_rules([], ["^apps\.common\.utils\.fields\.CountryField"])