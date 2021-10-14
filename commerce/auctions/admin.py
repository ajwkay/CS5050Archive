from django.contrib import admin
from .models import Bids, Listings, Comments

# Register your models here.
admin.site.register(Bids)
admin.site.register(Listings)
admin.site.register(Comments)
