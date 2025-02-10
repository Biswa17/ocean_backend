from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Port
from .serializers import PortSerializer

class PortList(APIView):
    """
    List all ports or create a new port.
    """
    def get(self, request):
        ports = Port.objects.all()
        serializer = PortSerializer(ports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PortDetail(APIView):
    """
    Retrieve, update or delete a port by ID.
    """
    def get(self, request, id):
        try:
            port = Port.objects.get(pk=id)
        except Port.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PortSerializer(port)
        return Response(serializer.data)
