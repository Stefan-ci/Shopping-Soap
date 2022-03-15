from profils.models import Profile
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

try:
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
except:
    pass

try:
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.profile:
            instance.profile.save()
except:
    pass
