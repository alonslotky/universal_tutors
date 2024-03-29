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

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'code', 'type', 'start', 'end', 'discount_percentage', 'discount_fixed', 'valid', 'total_times', 'total_times_used')
    list_filter = ('type',)
    search_fields = ('description',)
    exclude = ('total_times_used',)
admin.site.register(Discount, DiscountAdmin)

class DiscountUserAdmin(admin.ModelAdmin):
    list_display = ('discount', 'user', 'active', 'used')
    list_filter = ('discount', 'user', 'active')
    search_fields = ('discount', 'user', 'user__first_name', 'user__last_name')
admin.site.register(DiscountUser, DiscountUserAdmin)


class EmailTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(EmailTemplate, EmailTemplateAdmin)

class TimezoneAdmin(admin.ModelAdmin):
    pass
admin.site.register(Timezone, TimezoneAdmin)

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


class DocumentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Document, DocumentAdmin)
