from django import forms


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
        Added 'placeholder' attribute by customizing the default widget.
        """
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['subject'].widget.attrs.update({'placeholder': 'Subject'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Message'})
        self.fields['message'].widget.attrs.update({'rows': '5'})
