from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    # image max height and width
    IMG_MAX_HEIGHT:int = 300
    IMG_MAX_WIDTH:int = 300

    # One user has one profile and one profile has one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Profile picture, default and directory that images are uploaded to when we upload a profile
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # change default behavior when printing profile
    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """ Resize image if it is larger than max size before saving """
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > self.IMG_MAX_HEIGHT or img.width > self.IMG_MAX_WIDTH:
            output_size = (self.IMG_MAX_WIDTH, self.IMG_MAX_HEIGHT)
            # resize image
            img.thumbnail(output_size)
            # save to filepath and overwrite larger image
            img.save(self.image.path)
