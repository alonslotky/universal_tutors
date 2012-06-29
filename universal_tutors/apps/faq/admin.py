from django.contrib import admin
from django.conf import settings
from models import *

class ChildFAQItem(admin.TabularInline):
    class Media:
        js = [
            'http://%s/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js' % settings.PROJECT_SITE_DOMAIN,
            'http://%s/static/grappelli/tinymce_setup/tinymce_setup.js' % settings.PROJECT_SITE_DOMAIN,
        ]
    model = FAQItem
    extra = 2

class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ('section', 'position')
    list_editable = ['position']
    inlines = [ ChildFAQItem ]
admin.site.register(FAQSection, FAQSectionAdmin)

class FAQItemAdmin(admin.ModelAdmin):
    class Media:
        js = [
            'http://%s/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js' % settings.PROJECT_SITE_DOMAIN,
            'http://%s/static/grappelli/tinymce_setup/tinymce_setup.js' % settings.PROJECT_SITE_DOMAIN,
        ]
    list_display = ('question','section','position',)
    list_editable = ['section', 'position']
admin.site.register(FAQItem, FAQItemAdmin)



