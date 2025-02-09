# users/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .serializers import UserSerializer, RegisterSerializer
from .models import User, Organization

# Register view (using CreateAPIView)
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Hardcoded organization lookup for "Bata"
            organization = Organization.objects.filter(organization_name="Bata").first()
            # Create user with the "Bata" organization (if found), else None
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                phone_number=validated_data["phone_number"],
                organization=organization,  # Assign "Bata" organization if found
                password=validated_data["password"]
            )

            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view (using APIView)
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# User Details view (using RetrieveAPIView)
class UserDetailsView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Return the current logged-in user
