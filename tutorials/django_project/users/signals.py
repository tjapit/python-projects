from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# when a user is saved, a signal is sent and received by this receiver (create_profile function)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """ Creates a Profile whenever a User is created """
    # if the user was created
    if created:
        # create a Profile object with the user that was just created
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """ Saves the Profile whenever a User updates it """
    instance.profile.save()