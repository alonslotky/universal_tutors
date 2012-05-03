from django.contrib import admin
from django.contrib.auth.models import User
from models import *

class ClassAdmin(admin.ModelAdmin):
    list_display = ('subject', 'tutor', 'date', 'start', 'credit_fee', 'status')
admin.site.register(Class, ClassAdmin)

class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject',)
admin.site.register(ClassSubject, ClassSubjectAdmin)
