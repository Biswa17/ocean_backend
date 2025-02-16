from django.urls import path
from .views import create_cargo, list_cargo, update_cargo,create_container, list_containers, update_container

urlpatterns = [
    path('create-cargo/', create_cargo, name='create_cargo'),
    path('get-cargo/', list_cargo, name='list_cargo'),  # Handles both `/cargo/` and `/cargo`
    path('update-cargo/<int:id>/', update_cargo, name='update_cargo'),



    # Container API
    path('create-container/', create_container, name='create_container'),
    path('get-container/', list_containers, name='list_containers'),
    path('update-container/<int:id>/', update_container, name='update_container'),
]