from django import forms
from services.models import Service, Project, ProjectImages
from contact.models import Reviews, ContactDetails
from blog.models import Blog, BlogImage, Quotation
from aboutus.models import About
from .models import Profile
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

class ServiceForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Service Name", "class": "form-control"}),
        min_length=3,  # Minimum length validation
        max_length=100,  # Maximum length validation
        error_messages={
            'required': 'Service Name is required',
            'min_length': 'Service Name must be at least 3 characters long',
            'max_length': 'Service Name cannot exceed 100 characters',
        }
    )

    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        error_messages={
            'required': 'Service Image is required',
            'invalid': 'Please upload a valid image file (JPEG, PNG)',
        }
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter Service Description", "class": "form-control"}),
        min_length=10,  # Minimum length validation
        error_messages={
            'required': 'Description is required',
            'min_length': 'Description must be at least 10 characters long',
        }
    )

    slug = forms.SlugField(
        widget=forms.TextInput(attrs={"placeholder": "Slug (If not auto-generated)", "class": "form-control"}),
        required=False,  # Slug is optional, so required=False
        error_messages={
            'invalid': 'Enter a valid slug (letters, numbers, underscores, or hyphens only)',
        }
    )

    class Meta:
        model = Service
        fields = "__all__"

    # Custom validation method for slug
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')

        if slug:
            # Ensure slug contains only valid characters
            if not re.match(r'^[a-zA-Z0-9_-]+$', slug):
                raise ValidationError('Slug can only contain letters, numbers, underscores, and hyphens.')

        return slug

class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Project Title", "class": "form-control"}),
        min_length=3,
        max_length=100,
        error_messages={
            'required': 'Project title is required',
            'min_length': 'Title must be at least 3 characters long',
            'max_length': 'Title cannot exceed 100 characters',
        }
    )

    client = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Client Name", "class": "form-control"}),
        min_length=3,
        max_length=100,
        error_messages={
            'required': 'Client name is required',
            'min_length': 'Client name must be at least 3 characters long',
            'max_length': 'Client name cannot exceed 100 characters',
        }
    )

    address = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Project Address", "class": "form-control"}),
        min_length=5,
        error_messages={
            'required': 'Project address is required',
            'min_length': 'Address must be at least 5 characters long',
        }
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Project Location", "class": "form-control"}),
        min_length=3,
        error_messages={
            'required': 'Project location is required',
            'min_length': 'Location must be at least 3 characters long',
        }
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter Project Description", "class": "form-control"}),
        min_length=10,
        error_messages={
            'required': 'Project description is required',
            'min_length': 'Description must be at least 10 characters long',
        }
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={
            'required': 'You must select a service for this project',
        }
    )

    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Slug (Auto-generated if left empty)", "class": "form-control"}),
        error_messages={
            'invalid': 'Enter a valid slug (letters, numbers, hyphens, or underscores only)',
        }
    )

    class Meta:
        model = Project
        fields = ['title', 'client', 'address', 'location', 'description', 'service', 'slug']

    # Custom validation for slug
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            if not re.match(r'^[a-zA-Z0-9_-]+$', slug):
                raise ValidationError('Slug can only contain letters, numbers, underscores, and hyphens.')
        return slug

class ProjectImagesForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
            "allow_multiple_selected": True  # Keeps the option for multiple selections visually
        }),
        required=False
    )

    class Meta:
        model = ProjectImages
        fields = ['image']


class ReviewsForm(forms.ModelForm):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter User Name"}),
        min_length=3,  # Minimum length validation
        max_length=50,  # Maximum length validation
        error_messages={
            'required': 'User Name is required',
            'min_length': 'User Name must be at least 3 characters long',
            'max_length': 'User Name cannot exceed 50 characters',
        }
    )
    
    review = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter Review"}),
        min_length=10,  # Minimum length validation
        error_messages={
            'required': 'Review is required',
            'min_length': 'Review must be at least 10 characters long',
        }
    )
    
    user_image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        required=False,
        error_messages={
            'invalid': 'Please upload a valid image file (JPEG, PNG)',
        }
    )

    class Meta:
        model = Reviews
        fields = "__all__"

class BlogForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Blog Title", "class": "form-control"}),
        min_length=5,  # Minimum length validation
        max_length=100,  # Maximum length validation
        error_messages={
            'required': 'Blog Title is required',
            'min_length': 'Blog Title must be at least 5 characters long',
            'max_length': 'Blog Title cannot exceed 100 characters',
        }
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter Content for Blog", "class": "form-control"}),
        min_length=20,  # Minimum length validation
        error_messages={
            'required': 'Content is required',
            'min_length': 'Content must be at least 20 characters long',
        }
    )
    
    quotes = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Quote for Blog", "class": "form-control"}),
        max_length=200,  # Maximum length validation
        error_messages={
            'max_length': 'Quote cannot exceed 200 characters',
        }
    )
    
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        error_messages={
            'required': 'Blog Image is required',
            'invalid': 'Please upload a valid image file (JPEG, PNG)',
        }
    )
    
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Slug (Auto-generated if left empty)", "class": "form-control"}),
        error_messages={
            'invalid': 'Enter a valid slug (letters, numbers, underscores, or hyphens only)',
        }
    )

    latest = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,  # Make sure it's not required if it's optional
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'quotes', 'image', 'latest', 'slug']

    # Custom validation method for slug
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')

        if slug:
            # Ensure slug contains only valid characters
            if not re.match(r'^[a-zA-Z0-9_-]+$', slug):
                raise ValidationError('Slug can only contain letters, numbers, underscores, and hyphens.')

        return slug


class BlogImagesForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control", 'allow_multiple_selected': True}),
        required=False,
        error_messages={
            'invalid': 'Please upload a valid image file (JPEG, PNG)',
        }
    )

    class Meta:
        model = BlogImage
        fields = ['image']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter First Name", "class": "form-control"}),
        min_length=2,  # Minimum length validation
        max_length=30,  # Maximum length validation
        error_messages={
            'required': 'First Name is required',
            'min_length': 'First Name must be at least 2 characters long',
            'max_length': 'First Name cannot exceed 30 characters',
        }
    )
    
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Last Name", "class": "form-control"}),
        min_length=2,  # Minimum length validation
        max_length=30,  # Maximum length validation
        error_messages={
            'required': 'Last Name is required',
            'min_length': 'Last Name must be at least 2 characters long',
            'max_length': 'Last Name cannot exceed 30 characters',
        }
    )
    
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter Your Info!", "class": "form-control"}),
        max_length=500,  # Maximum length validation
        error_messages={
            'max_length': 'Bio cannot exceed 500 characters',
        }
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter Your Email", "class": "form-control"}),
        error_messages={
            'required': 'Email is required',
            'invalid': 'Enter a valid email address',
        }
    )
    
    address = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Your Current Address", "class": "form-control"}),
        max_length=255,  # Maximum length validation
        error_messages={
            'max_length': 'Address cannot exceed 255 characters',
        }
    )
    
    profile_image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        required=False,  # Make this optional
        error_messages={
            'invalid': 'Please upload a valid image file (JPEG, PNG)',
        }
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'bio', 'address', 'profile_image']


class ContactDetailsForm(forms.ModelForm):
    phone_no = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Enter Your Phone No!", 
            "class": "form-control"
        }),
        required=True,
        max_length=20,
        validators=[RegexValidator(
            regex=r'^[\+\d\s-]{9,20}$',  # allows +, digits, spaces, and hyphens
            message="Phone number can contain digits, spaces, hyphens, and may start with '+'."
        )],
        error_messages={
            'required': 'Phone No. is required',
            'max_length': 'Phone No. cannot exceed 20 characters',
        }
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter Your Email!", 
            "class": "form-control"
        }),
        required=True,
        max_length=50,
        error_messages={
            'required': 'This field is required',
            'max_length': 'Email cannot exceed 50 characters',
        }
    )

    office_location = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Enter Your Office Location", 
            "class": "form-control"
        }),
        required=True,
        max_length=100,
        error_messages={
            'required': 'This field is required',
            'max_length': 'Office Location cannot exceed 100 characters',
        }
    )

    class Meta:
        model = ContactDetails
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        phone_no = cleaned_data.get('phone_no')
        if phone_no:
            # Check if the phone number contains invalid characters
            if any(char not in '0123456789+ -' for char in phone_no):
                self.add_error('phone_no', "Phone number can only contain digits, spaces, hyphens, and may start with '+'.")
            # Check the length of the cleaned phone number
            if len(phone_no) < 9 or len(phone_no) > 20:
                self.add_error('phone_no', "Phone number must be between 9 and 20 characters long.")

        return cleaned_data

class AboutUsForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter About Description", "class": "form-control"}),
        max_length=150,  # Maximum length validation
        error_messages={
            'required': 'About Description is required',
            'max_length': 'Service Name cannot exceed 150 characters',
        }
    )

    company_info = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter About Company Info", "class": "form-control"}),
        error_messages={
            'required': 'About Description is required',
        }
    )

    mission = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Our Mission", "class": "form-control"}),
        max_length=250,  # Maximum length validation
        error_messages={
            'required': 'About Description is required',
            'max_length': 'Mission cannot exceed 250 characters',
        }
    )

    vision = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Our Vision", "class": "form-control"}),
        max_length=250,  # Maximum length validation
        error_messages={
            'required': 'About Description is required',
            'max_length': 'Service Name cannot exceed 250 characters',
        }
    )

    class Meta:
        model = About
        fields = "__all__"

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['quote', 'person_name']