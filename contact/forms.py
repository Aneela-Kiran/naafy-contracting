from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter your name", "class": "form-control"}),
        min_length=3,
        max_length=100,
        error_messages={
            'required': 'Name is required',
            'min_length': 'Name must be at least 3 characters',
            'max_length': 'Name cannot exceed 100 characters',
        }
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email", "class": "form-control"}),
        error_messages={
            'required': 'Email is required',
            'invalid': 'Enter a valid email address',
        }
    )
    phone_no = forms.CharField(
        widget=forms.NumberInput(attrs={"placeholder": "Enter the Phone No.", "class": "form-control"}),
        min_length=11,
        max_length=20,
        error_messages={
            'required': 'Phone No is required',
            'min_length': 'Phone No must be at least 11 characters',
            'max_length': 'Subject cannot exceed 20 characters',
        }
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter the subject", "class": "form-control"}),
        min_length=5,
        max_length=150,
        error_messages={
            'required': 'Subject is required',
            'min_length': 'Subject must be at least 5 characters',
            'max_length': 'Subject cannot exceed 150 characters',
        }
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter your message", "class": "form-control"}),
        min_length=10,
        error_messages={
            'required': 'Message is required',
            'min_length': 'Message must be at least 10 characters long',
        }
    )

    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
