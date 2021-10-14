from django.contrib import admin
from .models import User, Profiles, Stories, Reviews, Comments, PlaylistEntry

# Register your models here.
admin.site.register(User)
admin.site.register(Profiles)
admin.site.register(Stories)
admin.site.register(Reviews)
admin.site.register(Comments)
admin.site.register(PlaylistEntry)
