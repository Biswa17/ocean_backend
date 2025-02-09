# users/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .serializers import UserSerializer, RegisterSerializer
from .models import User, Organization
from ocean_management_system.utils.response import custom_response

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

            print(validated_data)
            
            
        if not organization:
            # Hardcode organization lookup for "Bata"
            organization = Organization.objects.filter(organization_name="Bata").first()

            # Create user with the "Bata" organization (if found), else None
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                phone_number=validated_data["phone_number"],
                organization=organization,  # Assign "Bata" organization if found
                password=validated_data["password"]
            )

            # Modify response variables
            response = {"user_id": user.id, "username": user.username}
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
                status = drf_status.HTTP_200_OK
                message = "Login successful"
            else:
                # Modify response variables on invalid password
                response = {"error": "Invalid credentials"}
                status = drf_status.HTTP_401_UNAUTHORIZED
                message = "Invalid credentials"

        except User.DoesNotExist:
            # Modify response variables when user is not found
            response = {"error": "User not found"}
            status = drf_status.HTTP_404_NOT_FOUND
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