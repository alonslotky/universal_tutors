from django import forms

from models import *


class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 54}), required=True)

#class FeedbackForm(forms.ModelForm):
#    class Meta:
#        model = FeedbackQuestionAnswer

#class FeedbackForm(forms.ModelForm):

#    question_1 = forms.CharField(widget=forms.Select(choices=[('', 'Please select...')] + list(Feedback.QUESTION_CHOICES)))
#    question_2 = forms.CharField(widget=forms.Select(choices=[('', 'Please select...')] + list(Feedback.QUESTION_2_CHOICES)))
#    question_3 = forms.CharField(widget=forms.Select(choices=[('', 'Please select...')] + list(Feedback.QUESTION_CHOICES)))
#    question_4 = forms.CharField(widget=forms.Select(choices=[('', 'Please select...')] + list(Feedback.QUESTION_CHOICES)))
    
#    class Meta:
#        model = Feedback
        