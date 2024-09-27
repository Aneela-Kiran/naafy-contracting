from django.db import models

# Create your models here.
class About(models.Model):
    description = models.CharField(max_length=150)
    company_info = models.TextField()
    mission = models.CharField(max_length=250)
    vision = models.CharField(max_length=250)

    def __str__(self) -> str:
        return "About us page content"