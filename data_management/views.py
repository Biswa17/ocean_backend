import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from ocean_management_system.utils.response import custom_response
from .serializers import ImageUploadSerializer

@api_view(['POST'])
def upload_image(request):
    response, status, message = [], 200, ""

    try:
        # Validate request data using serializer
        serializer = ImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return custom_response(serializer.errors, 400, "Invalid data")

        image = serializer.validated_data['image']
        image_type = serializer.validated_data['type']

        # Sanitize file name and folder to prevent path traversal
        safe_filename = os.path.basename(image.name)
        safe_folder = os.path.basename(image_type)

        # Whitelist allowed folders (prevent unauthorized folder access)
        ALLOWED_FOLDERS = {"profile", "documents", "products", "user"}
        if safe_folder not in ALLOWED_FOLDERS:
            return custom_response({}, 400, "Invalid folder type")

        # Define a safe relative file path
        relative_path = os.path.join(safe_folder, safe_filename)

        # Save the image using Django's default storage
        saved_path = default_storage.save(relative_path, ContentFile(image.read()))

        # Construct the full media URL for access
        file_url = settings.MEDIA_URL + saved_path

        response = {"file_path": file_url}
        message = "Image uploaded successfully."
        status = 201

    except Exception as e:
        response = {}
        message = str(e)
        status = 500

    return custom_response(response, status, message)
