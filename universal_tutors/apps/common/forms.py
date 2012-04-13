from django import forms

from uni_form.helpers import FormHelper, Submit, Reset, Button
from uni_form.helpers import Layout, Fieldset, Row, HTML

class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
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

