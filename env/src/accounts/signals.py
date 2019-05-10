from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver, Signal

from .models import UserProfile


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#             UserProfile.objects.create(user=instance)
# signals.post_save.connect(create_user_profile, sender=User)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
# @receiver(post_save, sender=User)
