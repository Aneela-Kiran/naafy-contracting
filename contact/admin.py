from django.contrib import admin
from .models import Contact, Email, Reviews, ContactDetails
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "submitted_at"]

class EmailAdmin(admin.ModelAdmin):
    list_display = ["email", "sent_at"]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_name','user_image']

class ContactDetailsAdmin(admin.ModelAdmin):
    list_display = ["phone_no", "email", "office_location"]

admin.site.register(Contact, ContactAdmin)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(ContactDetails, ContactDetailsAdmin)