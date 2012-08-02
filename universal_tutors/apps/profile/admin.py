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
admin.site.unregister(User)
admin.site.register(User, AdminUserAdmin)


class TutorProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Details', {
            'fields': ('title', 'about', 'video', 'profile_image', 'date_of_birth', 'country', 'timezone',)
        }),
        ('CRB', {
            'fields': ('crb_file', 'crb_expiry_date',)
        }),
        ('Financial', {
            'fields': ('income', 'currency', 'paypal_email')
        }),
        ('Status', {
            'fields': ('featured', 'activated', 'activation_date',)
        }),
        ('Subjects', {
            'fields': ('subjects_list',)
        }),
        
    )
    readonly_fields = ['subjects_list', 'paypal_email', 'activation_date', 'activated']
    
    list_display = ('__unicode__', 'title', 'activated', 'crb_expiry_date', 'featured', 'profile_image_approved', 'about_approved', 'video_approved', 'qualification_documents_approved', 'avg_rate', 'no_reviews', 'classes_given', 'min_credits', 'max_credits', 'income', 'currency',)
    list_filter = ['activated', 'crb_expiry_date', 'featured', 'currency']
    list_editable = ['crb_expiry_date', 'featured', 'profile_image_approved', 'about_approved', 'video_approved', 'qualification_documents_approved']
admin.site.register(TutorProfile, TutorProfileAdmin)


class ParentProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Details', {
            'fields': ('profile_image', 'date_of_birth', 'country', 'timezone',)
        }),
        ('Financial', {
            'fields': ('currency',)
        }),
    )

    list_display = ('__unicode__', 'country', 'date_of_birth')
    list_filter = ['country']
    list_editable = []
admin.site.register(ParentProfile, ParentProfileAdmin)

#def user_link(obj):
#    return '<a href="/admin/auth/user/%s/">Open User Record</a>' % obj.id
    
#def profile_link(obj):
#    return '<a href="/admin/profile/userprofile/%s/">Open Main Profile Record</a>' % obj.id

#class StudentInterestInline(admin.StackedInline):
#    model = StudentInterest.user.profile

def date_of_birth_and_age(self):
    return "%s (%s yrs old)" % (self.date_of_birth, self.age)
date_of_birth_and_age.short_description = 'Date of Birth'
date_of_birth_and_age.allow_tags = True

def email_addy(self):
    return "<a href='mailto:%s'>%s</a>" % (self.user.email, self.user.email)
email_addy.short_description = 'Email'
email_addy.allow_tags = True

def student_interests(self):
    return "<a href='/admin/profile/studentinterest/?user=%s'>View</a>" % (self.user.id)
student_interests.short_description = 'Interests'
student_interests.allow_tags = True

class StudentProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Details', {
            'fields': ('profile_image', 'date_of_birth', 'country', 'timezone', )
        }),
        ('Financial', {
            'fields': ('currency',)
        }),
    )

    list_display = ('__unicode__', 'type', email_addy, date_of_birth_and_age, 'gender', 'currency', 'country', 'timezone', student_interests)
    list_filter = ['type', 'country']
    list_editable = []
    #inlines = [StudentInterestInline,]
    
    """def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "studentinterest":
            kwargs["queryset"] = StudentInterest.objects.filter(user=self.user)
        return super(StudentProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)"""
    
admin.site.register(StudentProfile, StudentProfileAdmin)
 
    
    
class BadReviewAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'student', 'student_email', 'related_class', 'text',)
    readonly_fields = ('tutor', 'student', 'student_email')
    exclude = ('user', )
    
admin.site.register(BadReview, BadReviewAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('violator', 'user', 'created', 'description')
admin.site.register(ReportedTutor, ReportAdmin)
admin.site.register(ReportedStudent, ReportAdmin)

class TopUpItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'credits', 'value', 'currency', 'status', 'created')
    list_filter = ('user', 'status', 'currency')
    search_fields = ('user', 'user__first_name', 'user__last_name')
admin.site.register(TopUpItem, TopUpItemAdmin)

class WithdrawItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'credits', 'value', 'currency', 'status', 'created')
    list_filter = ('user', 'status', 'currency')
    search_fields = ('user', 'user__first_name', 'user__last_name')
admin.site.register(WithdrawItem, WithdrawItemAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)

class StudentInterestAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentInterest, StudentInterestAdmin)


#class NewsletterSubscriptionAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)


