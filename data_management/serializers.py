from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
    type = serializers.CharField(max_length=255)


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    type = serializers.CharField(required=True)
