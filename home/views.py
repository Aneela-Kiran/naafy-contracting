from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import EmailForm
from services.models import Service
from blog.models import Blog

# Create your views here.
def home_page(request):
    services = Service.objects.all()
    blogs = Blog.objects.filter(latest=True)
    context = {
        'services' : services,
        'blogs' : blogs,
    }

    return render(request, "home/index.html", context)

def save_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['email_submitted'] = True
            return JsonResponse({'status': 'success', 'message': 'Email saved successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Email Already Present!!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request!'})