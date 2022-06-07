from django.contrib import admin
from .models import Post

# register our own models into the admin page
admin.site.register(Post)
