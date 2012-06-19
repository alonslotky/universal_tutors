from django.contrib import admin
from django.contrib.auth.models import User
from models import *

class ClassAdmin(admin.ModelAdmin):
    list_display = ('subject', 'tutor', 'date', 'duration', 'credit_fee', 'status')
admin.site.register(Class, ClassAdmin)

class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject',)
admin.site.register(ClassSubject, ClassSubjectAdmin)

class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('system', 'level',)
admin.site.register(ClassLevel, ClassLevelAdmin)

class ChildCountries(admin.TabularInline):
    model = EducationalSystemCountry
    extra = 2

class ChildLevels(admin.TabularInline):
    model = ClassLevel
    extra = 2

class ChildSubject(admin.TabularInline):
    model = ClassSubject
    extra = 2

class EducationalSystemAdmin(admin.ModelAdmin):
    list_display = ('system',)
    inlines = [ChildCountries, ChildLevels, ChildSubject]    
admin.site.register(EducationalSystem, EducationalSystemAdmin)
