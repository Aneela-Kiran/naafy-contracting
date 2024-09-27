import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import BlogImage, Blog

@receiver(pre_save, sender=Blog)
@receiver(pre_save, sender=BlogImage)
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
@receiver(post_delete, sender=Blog)
@receiver(post_delete, sender=BlogImage)
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
                    pass  # Skip the deletion to avoid breaking the code; or you can log this for debugging
