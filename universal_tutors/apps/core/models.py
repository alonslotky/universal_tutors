# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.conf import settings

from apps.common.utils.abstract_models import BaseModel
from apps.common.utils.model_utils import get_namedtuple_choices

from apps.classes.settings import CREDIT_VALUE
import urlparse

class Currency(BaseModel):
    class Meta:
        verbose_name_plural = 'Currencies'
    
    acronym = models.CharField(max_length=3, help_text='Example: GBP')
    name = models.CharField(max_length=25, help_text='Example: British pound')
    symbol = models.CharField(max_length=3, help_text='Example: £')
    value = models.FloatField(help_text='One to GBP')
    manual = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s' % (self.acronym, self.name)
    
    def credit_value(self):
        return CREDIT_VALUE * self.value


class Quote(models.Model):
    quote = models.TextField()
    
    def __unicode__(self):
        return self.quote


class Video(models.Model):
    description = models.CharField(max_length=30)
    url = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.active:
            Video.objects.filter(active = True).exclude(id = self.id).update(active = False)
        super(self.__class__, self).save(*args, **kwargs)

    def get_video_id(self):
        try:
            parsed = urlparse.urlparse(self.url)
            video_id = urlparse.parse_qs(parsed.query)['v'][0]
        except IndexError:
            if self.url.find('http://youtu.be/') > 0:
                video_id = self.url.replace('http://youtu.be/', '')
        except KeyError:
            if self.url.find('http://youtu.be/') > 0:
                video_id = self.url.replace('http://youtu.be/', '')
        return video_id
