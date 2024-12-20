from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Contact
from .models import ContactDetails
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings


# Create your views here.
def contact_us(request):
    contact_details = ContactDetails.objects.all().first()
    context = {
        "contact_details" : contact_details,
    }
    return render(request, "contact/contact-us.html", context)

@csrf_protect
def contact_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        message = request.POST.get("message")

        if name and email and message:
            # Save contact form details
            contact_instance = Contact.objects.create(
                name=name,
                email=email,
                phone_no=phone_no,
                message=message
            )

            # Prepare the email content
            email_subject = "Contact Form Submission"
            email_message = f"Name: {name}\nEmail: {email}\nPhone No: {phone_no}\nMessage:\n{message}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = ['info@naafycontracting.ca', 'hamza.tahir.cs@gmail.com', 'naeem.toheed70@gmail.com', 'muh.ahmednoor@gmail.com']

            try:
                send_mail(
                    email_subject, email_message, from_email, recipient_list, fail_silently=False,
                )
                messages.success(request, "Message Sent Successfully!")
            except Exception as e:
                # Log or print the exception to help debug the issue
                print(f"Error sending email: {e}")
                messages.error(request, "There was an error sending your message. Please try again later.")

            return redirect(request.META.get('HTTP_REFERER', 'contact:contactus'))
        else:
            messages.warning(request, "Please fill in all required fields.")
    return render(request, "contact/contact-us.html")