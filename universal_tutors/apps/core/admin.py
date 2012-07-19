from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from flatblocks.models import FlatBlock
from flatblocks.admin import FlatBlockAdmin

from tinymce.widgets import TinyMCE

from apps.core.models import *

class TinyMCEFlatPageAdmin(FlatPageAdmin):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)


class TinyMCEFlatBlockAdmin(FlatBlockAdmin):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
admin.site.unregister(FlatBlock)
admin.site.register(FlatBlock, TinyMCEFlatBlockAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'name', 'symbol', 'manual', 'value')
admin.site.register(Currency, CurrencyAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('description', 'url', 'active')
    list_filter = ('type',)
admin.site.register(Video, VideoAdmin)
admin.site.register(Quote)

class BundleAdmin(admin.ModelAdmin):
    list_display = ('credits', 'discount')
admin.site.register(Bundle, BundleAdmin)


class EmailTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(EmailTemplate, EmailTemplateAdmin)


class CountryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Timezones', {
            'fields': ('timezones',)
        }),
    )

    list_display = ['country_name', 'list_timezones']
    filter_horizontal = ['timezones']
    search_fields = ['country_name', 'country']
admin.site.register(Country, CountryAdmin)


