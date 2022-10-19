from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    """ 
    This created flag will return when the profile is created, when some object is created.
    created flag will return True when the user is created, when some object is created, so otherwise it will return False.
    the sender instance is passed as created parameter to this post_save_receiver.

    and then connect this receiver to the sender.
    At here Sender is the user model

    """
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)



@receiver(pre_save, sender=User)
def pre_save(sender, instance, **kwargs):
    #trigger before the user is created
    pass


# post_save.connect(post_save_create_profile_receiver, sender=User)