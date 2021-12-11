from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Userprofile


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        # pylint: disable=maybe-no-member
        Userprofile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.profile.save()
