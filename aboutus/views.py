from django.shortcuts import render
from .models import About

# Create your views here.
def aboutus_view(request):
    aboutus = About.objects.all().order_by("-id")
    context = {
        "about" : aboutus,
    }
    return render(request, "aboutus/about-us.html", context)