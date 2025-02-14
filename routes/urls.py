from django.urls import path
from .views import get_routes, get_route_by_id

urlpatterns = [
    path('routes/', get_routes, name='get_routes'),  # URL to get all routes
    path('routes/<int:route_id>/', get_route_by_id, name='get_route_by_id'),  # URL to get route by ID
]
