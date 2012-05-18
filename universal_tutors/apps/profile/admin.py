from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class AdminUserAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','date_joined','last_login','is_staff', 'is_active')
    list_editable = ['is_active']
    inlines = [ UserProfileInline ]

class UTUserAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','date_joined','last_login',)
    list_editable = []
    inlines = [ UserProfileInline ]



admin.site.unregister(User)
admin.site.register(User, AdminUserAdmin)
admin.site.register(Tutor, UTUserAdmin)
admin.site.register(TutorList, UTUserAdmin)
admin.site.register(Student, UTUserAdmin)
admin.site.register(Parent, UTUserAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('violator', 'user', 'created', 'description')
admin.site.register(ReportedTutor, ReportAdmin)
admin.site.register(ReportedStudent, ReportAdmin)

class TopUpItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'credits', 'value', 'currency', 'status')
admin.site.register(TopUpItem, TopUpItemAdmin)

#class NewsletterSubscriptionAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)


