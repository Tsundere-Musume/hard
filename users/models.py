from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')
    banner = models.ImageField(default='default_banner.jpg', upload_to='banners')
    creationDate = models.DateField(auto_now_add=True)
    theme = models.CharField(max_length=5)

    def __str__(self):
        return (f'{self.user.username}\'s profile')
