from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass

class Bids(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.value} by {self.user}"

class Comments(models.Model):
    body = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments", default=1)

class Listings(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=1200)
    category = models.CharField(max_length=20, blank=True, null=True)
    img_url = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listing", default=1)
    highest_bid = models.OneToOneField(Bids, on_delete=models.DO_NOTHING, related_name="listing", null=True, blank=True)
    comments = models.ManyToManyField(Comments, related_name="comments", blank=True)
    open = models.BooleanField(default=True)

class Watchlist(models.Model):
    listing = models.ManyToManyField(Listings, related_name="watchlist", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist", default=1)
