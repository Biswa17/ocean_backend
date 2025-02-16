from django.urls import path
from .views import create_cargo, list_cargo, update_cargo

urlpatterns = [
    path('create-cargo/', create_cargo, name='create_cargo'),
    path('get-cargo/', list_cargo, name='list_cargo'),  # Handles both `/cargo/` and `/cargo`
    path('update-cargo/<int:id>/', update_cargo, name='update_cargo'),
]