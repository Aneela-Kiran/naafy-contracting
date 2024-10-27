from django.contrib import admin
from .models import Service, Project, ProjectImages
# Register your models here.

class ProjectImageInline(admin.TabularInline):
    model = ProjectImages
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('title', 'service', 'client', 'address', 'location')
    search_fields = ('title', 'client')
    prepopulated_fields = {"slug": ("title",)}

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Service, ServiceAdmin)
admin.site.register(Project, ProjectAdmin)