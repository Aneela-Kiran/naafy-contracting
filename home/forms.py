from django import forms
from contact.models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ["email"]