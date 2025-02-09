# oms_backend/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the user associated with the JWT token
        user = request.user

        # You can return some details about the user
        return Response({
            "message": "You have access to this protected view!",
            "user_id": user.id,
            "username": user.username
        })
