from django.db.models.signals import pre_save
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


@receiver(pre_save, sender=MyUser)
def delete_previous_avatar(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_avatar = MyUser.objects.get(pk=instance.pk).avatar
    except MyUser.DoesNotExist:
        return False

    new_avatar = instance.avatar
    if not old_avatar == new_avatar :
        if os.path.isfile(old_avatar.path) and old_avatar.path != DEFAULT_IMAGE_PATH:
            os.remove(old_avatar.path)
