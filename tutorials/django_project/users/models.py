from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # One user has one profile and one profile has one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Profile picture, default and directory that images are uploaded to when we upload a profile
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # change default behavior when printing profile
    def __str__(self) -> str:
        return f'{self.user.username} Profile'
