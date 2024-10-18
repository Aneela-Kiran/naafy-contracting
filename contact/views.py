from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Contact
from .models import Reviews, ContactDetails
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def contact_us(request):
    reviews = Reviews.objects.all().order_by("-id")
    contact_details = ContactDetails.objects.all().first()
    context = {
        "reviews" : reviews,
        "contact_details" : contact_details,
    }
    return render(request, "contact/contact-us.html", context)

@csrf_protect
def contact_form(request):
    # Handle form submission
    if request.method == "POST":
        # Fetching data from the request
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        message = request.POST.get("message")

        # Simple validation
        if name and email and message:  # You can add more validation if needed
            # Create and save the Contact instance
            contact_instance = Contact.objects.create(
                name=name,
                email=email,
                phone_no=phone_no,
                message=message
            )

            # Prepare email content
            email_subject = f"New Contact Form Submission"
            email_message = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone No: {phone_no}\n"
                f"Message:\n{message}"
            )
            recipient_list = ['sycode4j@gmail.com', 'hamza.tahir.cs@gmail.com'] 
            send_mail(email_subject, email_message, 'info@naafycontracting.ca', recipient_list)

            messages.success(request, "Message Sent Successfully!")
            return redirect("contact:contactus")  # Redirect after successful submission
        else:
            messages.warning(request, "Please fill in all required fields.")
    else:
        # For GET requests, just render the form
        return render(request, "contact/contact-us.html")