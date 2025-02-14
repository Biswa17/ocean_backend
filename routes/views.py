from rest_framework.decorators import api_view
from rest_framework.response import Response
from ocean_management_system.utils.response import custom_response
from .models import Route
from .serializers import RouteSerializer
from rest_framework.pagination import PageNumberPagination

# Get all routes
@api_view(['GET'])
def get_routes(request):
    response = []
    status = 200
    message = ""

    try:
        # Pagination settings (page and per_page from query params)
        page = request.GET.get('page', 1)  # Default page is 1
        per_page = request.GET.get('per_page', 10)  # Default per_page is 10

        # Implementing pagination
        paginator = PageNumberPagination()
        paginator.page_size = int(per_page)

        # Get all routes (without pagination)
        routes = Route.objects.all().order_by('id')

        # Paginate the queryset
        paginated_routes = paginator.paginate_queryset(routes, request)

        # Serialize the paginated data
        serializer = RouteSerializer(paginated_routes, many=True)

        # Prepare response with paginated data
        response = {
            'total_items': paginator.page.paginator.count,  # Total items available
            'total_pages': paginator.page.paginator.num_pages,  # Total pages
            'current_page': page,  # Current page
            'per_page': per_page,  # Items per page
            'data': serializer.data  # The actual paginated data
        }
        message = "Routes fetched successfully."
    except Exception as e:
        status = 500
        message = f"Error fetching routes: {str(e)}"

    return custom_response(data=response, status=status, message=message)

# Get route by ID
@api_view(['GET'])
def get_route_by_id(request, route_id):
    response = []
    status = 200
    message = ""

    try:
        route = Route.objects.get(id=route_id)
        serializer = RouteSerializer(route)
        response = serializer.data
        message = "Route fetched successfully."
    except Route.DoesNotExist:
        status = 404
        message = "Route not found."
    except Exception as e:
        status = 500
        message = f"Error fetching route: {str(e)}"

    return custom_response(data=response, status=status, message=message)
