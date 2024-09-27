import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import ProjectImages, Service, GeneralContracting

# Signal to delete old image before updating the instance

@receiver(pre_save, sender=GeneralContracting)
@receiver(pre_save, sender=ProjectImages)
@receiver(pre_save, sender=Service)
def delete_old_image_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = sender.objects.get(pk=instance.pk).image
        except sender.DoesNotExist:
            return
        new_image = instance.image
        if old_image and old_image != new_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

# Signal to delete image after deleting the instance

@receiver(post_delete, sender=GeneralContracting)
@receiver(post_delete, sender=ProjectImages)
@receiver(post_delete, sender=Service)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = sender.objects.get(pk=instance.pk).image
        except sender.DoesNotExist:
            return
        
        new_image = instance.image
        if old_image and old_image != new_image:  # Only delete if a new image is uploaded
            if os.path.isfile(old_image.path):
                try:
                    os.remove(old_image.path)
                except PermissionError:
                    pass 
