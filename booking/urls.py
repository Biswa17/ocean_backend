from django.urls import path
from .views import create_booking_with_id, list_booking, booking_detail, update_booking,create_tracking,get_tracking_details,create_booking_full_info

urlpatterns = [
    path('create-booking-with-id/', create_booking_with_id, name='create_booking'),
    path('create-booking-all-info/', create_booking_full_info, name='create_booking_full_info'),
    path('get-booking/', list_booking, name='list_booking'),
    path('get-booking/<int:id>/', booking_detail, name='booking_detail'),
    path('update-booking/<int:id>', update_booking, name='update_booking'),

    path('create-tracking/', create_tracking, name='create_tracking'),  # Create tracking
    path('get-tracking/<int:id>/', get_tracking_details, name='get_tracking_details'),  # Get tracking details
]
