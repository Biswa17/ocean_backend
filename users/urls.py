# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/', views.UserDetailsView.as_view(), name='user_details'),
    path('update/', views.UpdateUserView.as_view(), name='user_update'),
]
