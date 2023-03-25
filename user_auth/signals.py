from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import MyUser
import os

DEFAULT_IMAGE_PATH = os.path.join(settings.MEDIA_ROOT, "default.png")

# events
@receiver(post_delete, sender=MyUser)
def event_delete_handler(sender, instance, **kwargs):
    if instance.avatar and instance.avatar.path != DEFAULT_IMAGE_PATH:
        instance.avatar.delete(save=False)
