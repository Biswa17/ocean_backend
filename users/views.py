# users/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .serializers import UserSerializer, RegisterSerializer,ChangePasswordSerializer
from .models import User, Organization
from ocean_management_system.utils.response import custom_response
from django.contrib.auth.hashers import check_password

# Register view (using CreateAPIView)
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        # Initialize response, status, and message
        response = []
        status = 200
        message = ""

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            # Check if organization is provided, if not, assign "Bata"
            organization = validated_data.get("organization", None)
            if not organization:
                organization = Organization.objects.filter(organization_name="Bata").first()

            # Create the user with the organization (either provided or "Bata")
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                phone_number=validated_data["phone_number"],
                organization=organization,  # Assign "Bata" if organization is not provided
                password=validated_data["password"]
            )
            
            # Prepare the response with user details
            response = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number
            }
            
            # Define the status and message for the response
            status = 201
            message = "User created successfully"
        else:
            # Modify response variables in case of error
            response = serializer.errors
            status = 400
            message = "Bad request. Please check your input."

        # Return the standardized response using custom_response
        return custom_response(data=response, status=status, message=message)

# Login view (using APIView)
class LoginView(APIView):
    def post(self, request):
        # Initialize response, status, and message
        response = []
        status = 200
        message = ""

        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)

                # Modify response variables on success
                response = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                status = 200
                message = "Login successful"
            else:
                # Modify response variables on invalid password
                response = {"error": "Invalid credentials"}
                status = 401
                message = "Invalid credentials"

        except User.DoesNotExist:
            # Modify response variables when user is not found
            response = {"error": "User not found"}
            status = 400
            message = "User not found"

        # Return the standardized response using custom_response
        return custom_response(data=response, status=status, message=message)


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Initialize response, status, and message
        response = []
        status = 200
        message = ""

        user = request.user  # Access the current logged-in user

        # Serialize user data
        serializer = UserSerializer(user)

        # Modify response variables
        response = serializer.data
        status = 200
        message = "User details retrieved successfully"

        # Return the standardized response using custom_response
        return custom_response(data=response, status=status, message=message)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Initialize response, status, and message
        response = []
        status = 200
        message = ""

        # Get the authenticated user
        user = request.user
        # Allowed fields that can be updated
        allowed_fields = {"first_name", "last_name", "email", "phone_number", "user_profile_image"}

        # Extract provided data
        updated_data = request.data

        # Extract existing data
        serializer = UserSerializer(user)
        existing_data = serializer.data

        # Identify fields that actually need an update, excluding restricted fields
        fields_to_update = {
            key: updated_data[key]
            for key in updated_data
            if key in allowed_fields and str(existing_data.get(key)) != str(updated_data[key])
        }

        if not fields_to_update:
            return custom_response(data=existing_data, status=200, message="No changes detected")

        # Perform a partial update with only changed fields
        serializer = UserSerializer(user, data=fields_to_update, partial=True)

        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            message = "User details updated successfully"
        else:
            response = serializer.errors
            status = 400
            message = "Validation failed"

        # Return the standardized response using custom_response
        return custom_response(data=response, status=status, message=message)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Initialize response, status, and message
        response = []
        status_code = 200
        message = ""

        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            # Verify old password
            if not check_password(old_password, user.password):
                return custom_response(data={}, status=400, message="Old password is incorrect")

            # Update password
            user.set_password(new_password)
            user.save()

            response = {"success": True}
            message = "Password changed successfully"
        else:
            response = serializer.errors
            status_code = 400
            message = "Validation failed"

        # Return the standardized response
        return custom_response(data=response, status=status_code, message=message)