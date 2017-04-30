from django import forms


class ContactForm(forms.Form):
    """
    Base contact form class.
    """
    # name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    subject = forms.CharField(required=True, max_length=200)
    message = forms.CharField(required=True, widget=forms.Textarea)

