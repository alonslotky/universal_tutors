from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class MyUserAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','date_joined','last_login','is_staff', 'is_active')
    list_editable = ['is_active']
    inlines = [ UserProfileInline ]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Tutor, MyUserAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('violator', 'user', 'created', 'description')
admin.site.register(Report, ReportAdmin)

#class NewsletterSubscriptionAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)


