from rest_framework import status
from rest_framework.views import APIView
from .models import Port
from .serializers import PortSerializer
from ocean_management_system.utils.response import custom_response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

class PortList(APIView):
    """
    List all ports or create a new port.
    """
    def get(self, request):
        # Initialize response, status, and message
        response = []
        status_code = status.HTTP_200_OK
        message = "Ports retrieved successfully"

        search_term = request.GET.get('search', '')
        
        # Pagination settings (page and per_page from query params)
        page = request.GET.get('page', 1)  # Default page is 1
        per_page = request.GET.get('per_page', 10)  # Default per_page is 10

        # Implementing pagination
        paginator = PageNumberPagination()
        paginator.page_size = int(per_page)

        # Get all ports (without pagination)
        ports = Port.objects.all().order_by('port_name')
        if search_term and len(search_term) >= 3:
            ports = ports.filter(
                Q(port_name__icontains=search_term) |
                Q(country__icontains=search_term)
            )
        # Paginate the queryset
        paginated_ports = paginator.paginate_queryset(ports, request)

        # Serialize the paginated data
        serializer = PortSerializer(paginated_ports, many=True)

        
        # Prepare response with paginated data
        response = {
            'total_items': paginator.page.paginator.count,  # Total items available
            'total_pages': paginator.page.paginator.num_pages,  # Total pages
            'current_page': page,  # Current page
            'per_page': per_page,  # Items per page
            'data': serializer.data  # The actual paginated data
        }

        # Return paginated response
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
