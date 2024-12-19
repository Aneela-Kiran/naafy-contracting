from django.contrib import admin
from .models import Blog, BlogReply, BlogImage, Quotation
# Register your models here.
class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    list_display = ["title", "image", "slug", "created_at"]

admin.site.register(Blog, BlogAdmin)
admin.site.register(Quotation)
admin.site.register(BlogReply)