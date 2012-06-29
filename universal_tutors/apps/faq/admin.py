from django.contrib import admin
from models import *

class ChildFAQItem(admin.TabularInline):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
    list_display = ('question','section','position',)
    list_editable = ['position']
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
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
    list_display = ('question','section','position',)
    list_editable = ['position']
admin.site.register(FAQItem, FAQItemAdmin)



