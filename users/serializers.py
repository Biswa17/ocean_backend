from rest_framework import serializers
from .models import User, Organization
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())  # Use ID for organization
    first_name = serializers.CharField(source="username")
    user_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name','last_name', 'email', 'phone_number', 'organization','user_profile_image','user_position','is_active', 'is_admin']
    
    def get_user_profile_image(self, obj):
        if obj.user_profile_image:
            return f"{settings.BASE_URL}{obj.user_profile_image}"
        return None

class RegisterSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False, write_only=True
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'organization', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only

    def create(self, validated_data):
        organization = validated_data.pop('organization', None)  # Extract organization instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            organization=organization,
            password=validated_data['password']
        )
        return user
