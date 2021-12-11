from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from gigs.models import Gig


@receiver(post_save, sender=User)
def create_usergig(sender, instance, created, **kwargs):
    if created:
        # pylint: disable=maybe-no-member
        Gig.objects.create(user=instance)
    # Existing users: just save the profile
    instance.gig.save()
