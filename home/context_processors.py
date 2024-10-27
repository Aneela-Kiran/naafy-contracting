from contact.models import ContactDetails

def default(request):
    contact_details = ContactDetails.objects.first()

    return {
        "contact_details" : contact_details,
    }