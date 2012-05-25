from django.contrib import admin

from models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("/static/css/feedback.css",)
        }
    pass

admin.site.register(Feedback, FeedbackAdmin)