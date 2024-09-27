from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm
from django.http import JsonResponse
from .models import Reviews, ContactDetails

# Create your views here.
def contact_us(request):
    reviews = Reviews.objects.all().order_by("-id")
    contact_details = ContactDetails.objects.all().first()
    context = {
        "reviews" : reviews,
        "contact_details" : contact_details,
    }
    return render(request, "contact/contact-us.html", context)
    
def contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data to the database
            contact_instance = form.save()

            # Send email
            subject = f"New Contact Form Submission: {contact_instance.subject}"
            message = f"Name: {contact_instance.name}\nEmail: {contact_instance.email}\nPhone No:{contact_instance.phone_no}\nMessage:\n{contact_instance.message}"
            recipient_list = ['sycode4j@gmail.com','muh.ahmednoor@gmail.com'] 
            send_mail(subject, message, 'm.hamza.codes@gmail.com', recipient_list)

            # Set session flag to indicate the form was submitted
            request.session["form_submitted"] = True
            return JsonResponse({"status": "success", "message": "Form Submitted Successfully!!"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid Data! Please Fill the form Again!!"})
    return JsonResponse({"status": "error", "message": "Invalid Data! Please Fill the form Again!!"})