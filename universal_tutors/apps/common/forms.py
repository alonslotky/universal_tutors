from django import forms

from models import Feedback


class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 54}), required=True)

#    helper = FormHelper()
#    helper.form_tag = False
#    layout = Layout(
#        Fieldset('',
#            'name', 'email',
#        ),
#    )
#    helper.add_layout(layout)

    # Submit button(s)
#    button = Button('cancel','Cancel', css_class='secondaryAction')
#    helper.add_input(button)
#    submit = Submit('submit','Send', css_class='primaryAction')
#    helper.add_input(submit)


class FeedbackForm(forms.ModelForm):

    question_1 = forms.CharField(widget=forms.Select(choices=[('', 'Please select...')] + list(Feedback.QUESTION_CHOICES)))
    question_2 = forms.CharField(widget=forms.Select(choices=[('', 'Please select...')] + list(Feedback.QUESTION_2_CHOICES)))
    question_3 = forms.CharField(widget=forms.Select(choices=[('', 'Please select...')] + list(Feedback.QUESTION_CHOICES)))
    question_4 = forms.CharField(widget=forms.Select(choices=[('', 'Please select...')] + list(Feedback.QUESTION_CHOICES)))
    
    class Meta:
        model = Feedback
        