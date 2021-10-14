from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from uuid import uuid4
import os

@deconstructible
class PathAndScramble(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)

path_and_scramble = PathAndScramble(f"{settings.MEDIA_ROOT}reader/static/story_covers")
save_and_rename = PathAndScramble(f"{settings.MEDIA_ROOT}dummy_folder")

GENRE_TAGS = (
    ("", _("Select a genre...")),
    ("ROMANCE", _('Romance')),
    ("ADVENTURE", _('Adventure')),
    ("MYSTERY", _('Mystery')),
    ("SCI-FI", _('Sci-Fi')),
    ("NON-FICTION", _('Non-Fiction')),
    ("FANTASY", _('Fantasy')),
    ("COMEDY", _('Comedy')),
    ("DRAMA", _('Drama')),
    ("HORROR", _('Horror')),
    ("THRILLER", _('Thriller')),
    ("HISTORICAL", _('Historical'))
)

EDITOR_USED = (
    ("", _("---")),
    ("HypeDyn2", _("HypeDyn 2")),
    ("Twine", _("Twine")),
    ("Squiffy", _("Squiffy"))
)

RATINGS = (
    ("", _("-")),
    (1, _("1")),
    (2, _("2")),
    (3, _("3")),
    (4, _("4")),
    (5, _("5")),
    (6, _("6")),
    (7, _("7")),
    (8, _("8")),
    (9, _("9")),
    (10, _("10")),
)

PLAY_STATUS = (
    ("", _("--")),
    (1, _("Completed")),
    (2, _("Playing")),
    (3, _("Plan to Play")),
    (4, _("Dropped")),
)

class User(AbstractUser):
    pass

class Profiles(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    intro = models.CharField(max_length=10000)
    date_time_created = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="follow_list", blank=True)
    photo = models.ImageField(upload_to= settings.MEDIA_ROOT + "reader/static/library/profile_pictures", blank=True, null=True)

class Stories(models.Model):
    tags = models.CharField(max_length=20, choices=GENRE_TAGS, blank=False, default="")
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=10000, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="stories_written", blank=False, null=True, default="")
    favourited = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="stories_favourited", blank=True)
    date_time_submitted = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to = path_and_scramble, blank=True, null=True, default=f"{settings.MEDIA_ROOT}reader/static/story_covers/unknown.jpg")
    story_folder_id = models.CharField(max_length=50, blank=False, null=False, default=0)
    avg_rating = models.FloatField(blank=True, null=True, default=0)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="stories_bookmarked", blank=True)
    editor_used = models.CharField(max_length=10, choices=EDITOR_USED, blank=False, null=False, default="")

class Reviews(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="reviews_written", blank=False, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=False, default="")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="reviews_liked", blank=True)
    story = models.ForeignKey("Stories", on_delete=models.CASCADE, related_name="reviews", blank=False)
    body = models.CharField(max_length=5000, blank=False)
    date_time_posted = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="comments_written", blank=False, null=True)
    body = models.CharField(max_length=5000, blank=False)
    profile = models.ForeignKey("Profiles", on_delete=models.CASCADE, related_name="profile_comments", blank=True)
    date_time_posted = models.DateTimeField(auto_now_add=True)

class PlaylistEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="playlist_entry", blank=False)
    story = models.ForeignKey("Stories", on_delete=models.CASCADE, related_name="playlists_found_in", blank=True, null=True)
    play_status = models.IntegerField(blank=False, default="")

class DummyModel(models.Model):
    file_field = models.FileField(_("file"), upload_to=save_and_rename, blank=True, null=True, default=f'')

@receiver(models.signals.post_delete, sender=DummyModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file_field:
        if os.path.isfile(instance.file_field.path):
            os.remove(instance.file_field.path)

@receiver(models.signals.pre_save, sender=DummyModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = DummyModel.objects.get(pk=instance.pk).file_field
    except DummyModel.DoesNotExist:
        return False

    new_file = instance.file_field
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
