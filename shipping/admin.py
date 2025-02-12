from django.contrib import admin
from .models import Ship, ShippingLiner, ShippingRoutes

admin.site.register(Ship)
admin.site.register(ShippingLiner)
admin.site.register(ShippingRoutes)