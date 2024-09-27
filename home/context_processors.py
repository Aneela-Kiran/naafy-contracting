from services.models import Service
from contact.models import ContactDetails

def default(request):
    services = Service.objects.all().order_by("-id")
    contact_details = ContactDetails.objects.first()

    return {
        "services" : services,
        "contact_details" : contact_details,
    }