from rest_framework import serializers
from .models import User, Organization
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())  # Use ID for organization
    organization_name = serializers.SerializerMethodField()
    first_name = serializers.CharField(source="username")
    user_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'organization','organization_name', 'user_profile_image', 'user_position', 'is_active', 'is_admin']

    def __init__(self, *args, **kwargs):
        # Get 'fields' from context if provided, else return all fields
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    def get_organization_name(self, obj):
        """Fetch and return organization name."""
        return obj.organization.organization_name if obj.organization else None

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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
