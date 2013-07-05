from django.contrib import admin

from models import FeedbackQuestion, FeedbackQuestionOption, FeedbackAnswer

class FeedbackQuestionOptionsInline(admin.TabularInline):
    model = FeedbackQuestionOption
    
class FeedbackAnswerAdmin(admin.ModelAdmin):
    search_fields = ['question', 'option']
    list_filter = ['question', 'option',]

admin.site.register(FeedbackAnswer, FeedbackAnswerAdmin)

class FeedbackQuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'optional_text_title', 'position',]
    list_editable = ['position']
    inlines = [FeedbackQuestionOptionsInline]

admin.site.register(FeedbackQuestion, FeedbackQuestionAdmin)
