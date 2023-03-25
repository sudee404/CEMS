from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Event,Category,Guest, Speaker, Venue
import os

DEFAULT_IMAGE_PATH = os.path.join(settings.MEDIA_ROOT, "default.png")

# events
@receiver(post_delete, sender=Event)
def event_delete_handler(sender, instance, **kwargs):
    if instance.poster and instance.poster.path != DEFAULT_IMAGE_PATH:
        instance.poster.delete(save=False)
        
# venue
@receiver(post_delete, sender=Venue)
def event_delete_handler(sender, instance, **kwargs):
    if instance.poster and instance.poster.path != DEFAULT_IMAGE_PATH:
        instance.poster.delete(save=False)
        
# category
@receiver(post_delete, sender=Category)
def event_delete_handler(sender, instance, **kwargs):
    if instance.image and instance.image.path != DEFAULT_IMAGE_PATH:
        instance.image.delete(save=False)

# guests
@receiver(post_delete, sender=Guest)
def event_delete_handler(sender, instance, **kwargs):
    if instance.qr_code:
        instance.qr_code.delete(save=False)
        
# speaker
@receiver(post_delete, sender=Speaker)
def event_delete_handler(sender, instance, **kwargs):
    if instance.avatar and instance.avatar.path != DEFAULT_IMAGE_PATH:
        instance.avatar.delete(save=False)
