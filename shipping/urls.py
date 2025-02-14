from django.urls import path
from .views import ShipsByPortRoute

urlpatterns = [
    path('get-ships-by-port/', ShipsByPortRoute.as_view(), name='get-ships-by-port'),
]
