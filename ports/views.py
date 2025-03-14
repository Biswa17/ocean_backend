from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from .models import Port, Lane
from .serializers import PortSerializer
from ocean_management_system.utils.response import custom_response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from routes.models import RouteLanes
from shipping.models import ShippingRoutes
from  shipping.serializers import ShippingRoutesSerializer

class PortList(APIView):
    """
    List all ports or create a new port.
    """
    def get(self, request):
        # Initialize response, status, and message
        response = []
        status_code = 200
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_lane_availability(request):
    response = []
    status = 200
    message = ""

    try:
        from_port = request.GET.get('from_port')
        to_port = request.GET.get('to_port')
        departure_date = request.GET.get('departure_date', None)

        if not from_port or not to_port:
            status = 400
            message = "Both from_port and to_port are required."
            return custom_response(response, status, message)

        # Check if the lane exists
        lane = Lane.objects.filter(from_port_id=from_port, to_port_id=to_port).first()
        if not lane:
            status = 404
            message = "No lane found for the given ports."
            return custom_response(response, status, message)

        # Fetch routes by lane
        fetch_routes_by_lane = RouteLanes.objects.filter(lane=lane).values_list('route', flat=True)

        serviceable_routes = ShippingRoutes.objects.filter(route__in=fetch_routes_by_lane)

        if not serviceable_routes.exists():
            status = 404
            message = "No serviceable shipping routes available for the given lane."
            return custom_response(response, status, message)

        # Serialize the serviceable routes
        serialized_routes = ShippingRoutesSerializer(serviceable_routes, many=True).data  

        # Serialize response
        response = {
            "lane_id": lane.id,
            "serviceable_routes": serialized_routes
        }
        message = "Lane and shipping route availability retrieved successfully."

    except Exception as e:
        status = 500
        message = f"An error occurred: {str(e)}"

    return custom_response(response, status, message)