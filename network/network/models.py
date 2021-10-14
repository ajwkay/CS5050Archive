from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass

class Profiles(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles")
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="follow_list", blank=True)
    posts = models.ManyToManyField("Posts", related_name="profiles", blank=True)

    def __str__(self):
        return f"{self.user}'s profile"

class Posts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)
    body = models.CharField(max_length=1000)
    datetimestamp = models.DateTimeField(auto_now_add=True)
