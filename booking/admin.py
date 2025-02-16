from django.contrib import admin

from .models import Booking, Tracking,Document

admin.site.register(Booking)
admin.site.register(Tracking)
admin.site.register(Document)