from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
    type = serializers.CharField(max_length=255)
