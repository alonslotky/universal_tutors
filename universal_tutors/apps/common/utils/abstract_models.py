from django.db import models
from django.contrib.auth.models import User

from filebrowser.fields import FileBrowseField

from apps.common.utils.model_utils import unique_slugify
from apps.common.utils.geo import geocode_location

"""
    Abstract model classes that define common uses cases
"""

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return "%s" % self.id
        
class PhotoModel(BaseModel):
    submitted_by = models.ForeignKey(User)
    caption = models.TextField(blank=True, null=True)
    photo = FileBrowseField('Image (Initial Directory)', max_length=100, directory='uploads/')
    is_default = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
    
class TitleAndSlugModel(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True, help_text="The part of the title that is used in the url. Leave this blank if you want the system to generate one for you.")
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        
        return super(TitleAndSlugModel, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title
        
class GeoModelMixin(models.Model):
    postcode = models.CharField(max_length=10)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    
    __original_postcode = None
    
    class Meta:
        abstract = True
        
    def __init__(self, *args, **kwargs):
        super(GeoModelMixin, self).__init__(*args, **kwargs)
        self.__original_postcode = self.postcode
        
    def save(self, *args, **kwargs):
        if self.postcode != self.__original_postcode:
            self.latitude, self.longitude = geocode_location(self.postcode)
        return super(GeoModelMixin, self).save(*args, **kwargs)