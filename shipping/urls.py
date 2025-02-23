from django.urls import path
from .views import ShipsByPortRoute,get_voyage_from_booking

urlpatterns = [
    path('get-ships-by-port/', ShipsByPortRoute.as_view(), name='get-ships-by-port'),
    path('get-booking/<int:booking_id>/voyage/', get_voyage_from_booking, name='get-voyage'),
]
