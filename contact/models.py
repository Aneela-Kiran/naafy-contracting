from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20, default="+123 456 7890")
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Message from {self.name}"
    
class Email(models.Model):
    email = models.EmailField(unique=True, max_length=254)
    sent_at = models.DateTimeField(auto_now=True)
    responded = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Email from user"
    
class Reviews(models.Model):
    user_name = models.CharField(unique=True, max_length=250)
    review = models.TextField()

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name_plural = "Reviews"

class ContactDetails(models.Model):
    phone_no = models.CharField(max_length=20, default="+123 456 7890")
    email = models.EmailField(unique=True)
    office_location = models.CharField(max_length=100)

    def __str__(self):
        return self.email