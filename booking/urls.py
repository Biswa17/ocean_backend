from django.urls import path
from .views import create_cargo, list_cargo, update_cargo,create_booking, list_booking, booking_detail, update_booking,create_tracking,get_tracking_details

urlpatterns = [
    path('create-cargo/', create_cargo, name='create_cargo'),
    path('get-cargo/', list_cargo, name='list_cargo'),  # Handles both `/cargo/` and `/cargo`
    path('update-cargo/<int:id>/', update_cargo, name='update_cargo'),

    path('create-booking/', create_booking, name='create_booking'),
    path('get-booking/', list_booking, name='list_booking'),
    path('get-booking/<int:id>/', booking_detail, name='booking_detail'),
    path('update-booking/<int:id>', update_booking, name='update_booking'),

    path('create-trackin/', create_tracking, name='create_tracking'),  # Create tracking
    path('get-tracking/<int:id>/', get_tracking_details, name='get_tracking_details'),  # Get tracking details
]
