from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("", views.services_view, name="services"),
    path("general-services/", views.general_service_view, name="gen-services"),
    path("<slug:slug>/", views.service_projects, name="service-projects"),
]
