from time import time_ns
from django.db import models
from django.utils import timezone
# importing pre-existing User model from django
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # auto_now=True: datetime of last modified
    # auto_now_add=True: current datetime only when created **can't ever be updated
    # default=timezone.now: current datetime but mutable
    date_posted = models.DateTimeField(default=timezone.now)
    # User @OneToMany Post
    # on_delete=models.CASCADE: delete Post if User is deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
    