from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from core.models import UserExtension, IntranetMeta


@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)

@receiver(post_save, sender=IntranetMeta)
def toggle_lan_active(sender, instance, created, **kwargs):
    currentMeta = IntranetMeta.objects.get(pk=instance.pk)
    if currentMeta.active:
        metas = IntranetMeta.objects.all().exclude(pk=instance.pk)
        for meta in metas:
            meta.active = False
            meta.save()
