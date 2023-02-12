from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Event,Category
import os

DEFAULT_IMAGE_PATH = os.path.join(settings.MEDIA_ROOT, "default.png")


@receiver(post_delete, sender=Event)
def event_delete_handler(sender, instance, **kwargs):
    if instance.poster and instance.poster.path != DEFAULT_IMAGE_PATH:
        instance.poster.delete(save=False)
        

@receiver(post_delete, sender=Category)
def event_delete_handler(sender, instance, **kwargs):
    if instance.image and instance.image.path != DEFAULT_IMAGE_PATH:
        instance.image.delete(save=False)
