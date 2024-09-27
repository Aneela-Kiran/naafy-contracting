from django.contrib import admin
from .models import About
# Register your models here.
class AboutAdmin(admin.ModelAdmin):
    list_display = ["description","mission", "vision"]

admin.site.register(About, AboutAdmin)