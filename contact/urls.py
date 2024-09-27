from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("", views.contact_us, name="contactus"),
    path("contact-form/", views.contact_form, name="contact-form"),
]
