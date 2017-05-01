from django import forms
from django.urls import reverse

from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from crispy_forms.layout import Submit, Layout, Div, Fieldset


class ContactForm(forms.Form):
    """
    Base contact form class.
    """
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(required=True, max_length=100, label='Email')
    subject = forms.CharField(required=True, max_length=200, label='Subject')
    message = forms.CharField(required=True, widget=forms.Textarea, label='Message')

    def __init__(self, *args, **kwargs):
        """
        Crispy_form FormHelper which is responsible for customizing the form.
        """
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'contactForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-default'))







