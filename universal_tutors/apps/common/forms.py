from django import forms

from uni_form.helpers import FormHelper, Submit, Reset, Button
from uni_form.helpers import Layout, Fieldset, Row, HTML

TOPIC_CHOICES = (
     ('', '-----'),
     ('search', 'Search'),
     ('profiles', 'Profiles'),
     ('dashboard', 'Dashboard'),
     ('classroom', 'Classroom'),
     ('other', 'Other'),
)

class ContactForm(forms.Form):

    username = forms.CharField(required=True)
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    topic = forms.ChoiceField(choices=TOPIC_CHOICES, required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 54}), required=True)

    helper = FormHelper()
    helper.form_tag = False
    layout = Layout(
        Fieldset('',
            'type', 'name',
            'email', 'message',
        ),
    )
    helper.add_layout(layout)

    # Submit button(s)
    button = Button('cancel','Cancel', css_class='secondaryAction')
    helper.add_input(button)
    submit = Submit('submit','Send', css_class='primaryAction')
    helper.add_input(submit)

