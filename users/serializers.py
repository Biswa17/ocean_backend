from rest_framework import serializers
from .models import User, Organization

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())  # Use ID for organization

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'organization', 'is_active', 'is_admin']

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
