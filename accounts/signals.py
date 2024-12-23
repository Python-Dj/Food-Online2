from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("User Profile has been created.")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
            print("Your profile has been created, Thanks!")

        print("User is updated")