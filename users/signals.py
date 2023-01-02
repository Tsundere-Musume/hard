from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import MyUser

@receiver(post_save, sender=User)
def createMyUser(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def saveMyUser(sender, instance, **kwargs):
    instance.myuser.save()