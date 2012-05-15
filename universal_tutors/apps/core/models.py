# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.conf import settings

from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.model_utils import get_namedtuple_choices

from apps.classes.settings import CREDIT_VALUE

class Currency(BaseModel):
    class Meta:
        verbose_name_plural = 'Currencies'
    
    acronym = models.CharField(max_length=3, help_text='Example: GBP')
    name = models.CharField(max_length=25, help_text='Example: British pound')
    symbol = models.CharField(max_length=3, help_text='Example: £')
    value = models.FloatField(help_text='One to GBP')
    manual = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.acronym)
    
    def credit_value(self):
        return CREDIT_VALUE * self.value

