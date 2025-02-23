from django.urls import path
from .views import upload_image,upload_file

urlpatterns = [
    path('upload_images/', upload_image, name='upload_image'),
    path('upload-files/', upload_file, name='upload-file'),
]
