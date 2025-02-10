from rest_framework import status
from rest_framework.views import APIView
from .models import Port
from .serializers import PortSerializer
from ocean_management_system.utils.response import custom_response

class PortList(APIView):
    """
    List all ports or create a new port.
    """
    def get(self, request):
        # Initialize response, status, and message
        response = []
        status_code = status.HTTP_200_OK
        message = "Ports retrieved successfully"
        
        ports = Port.objects.all()
        serializer = PortSerializer(ports, many=True)
        
        response = serializer.data
        return custom_response(data=response, status=status_code, message=message)

    def post(self, request):
        # Initialize response, status, and message
        response = []
        status_code = 201
        message = "Port created successfully"
        
        serializer = PortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
        else:
            response = serializer.errors
            status_code = 400
            message = "Invalid data"
        
        return custom_response(data=response, status=status_code, message=message)

class PortDetail(APIView):
    """
    Retrieve, update or delete a port by ID.
    """
    def get(self, request, id):
        # Initialize response, status, and message
        response = []
        status_code = 200
        message = "Port details retrieved successfully"

        try:
            port = Port.objects.get(pk=id)
        except Port.DoesNotExist:
            response = {'detail': 'Not found.'}
            status_code = 404
            message = "Port not found"
            return custom_response(data=response, status=status_code, message=message)

        serializer = PortSerializer(port)
        response = serializer.data
        return custom_response(data=response, status=status_code, message=message)
