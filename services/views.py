from django.shortcuts import render, get_object_or_404
from .models import Service, Project, ProjectImages, GeneralContracting
from django.core.paginator import Paginator

# Create your views here.
def services_view(request):
    services = Service.objects.all()
    paginator = Paginator(services, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "services" : page_obj,
    }
    return render(request, "services/services.html", context)

def service_projects(request, slug):
    service = get_object_or_404(Service, slug=slug)
    projects = Project.objects.filter(service=service)
    
    # Pagination
    paginator = Paginator(projects, 1)  # Show 1 project per page
    page = request.GET.get('page')
    paginated_projects = paginator.get_page(page)

    # Collect images for all projects
    project_images = ProjectImages.objects.filter(project__in=paginated_projects)

    context = {
        "projects": paginated_projects,
        "project_images": project_images,
    }

    return render(request, "services/service-projects.html", context)

def general_service_view(request):
    gen_services = GeneralContracting.objects.all()
    paginator = Paginator(gen_services, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "gen_services" : page_obj,
    }
    return render(request, "services/general-services.html", context)
