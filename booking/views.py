from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cargo, Booking
from .serializers import CargoSerializer, BookingSerializer,BookingDetailSerializer
from ocean_management_system.utils.response import custom_response
from rest_framework.pagination import PageNumberPagination


@api_view(['POST'])
def create_cargo(request):
    response = []
    status = 200
    message = ""

    serializer = CargoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = serializer.data
        message = "Cargo created successfully."
    else:
        response = serializer.errors
        status = 400
        message = "Validation failed."

    return custom_response(response, status, message)

@api_view(['GET'])
def list_cargo(request):
    response = []
    status = 200
    message = ""

    cargo = Cargo.objects.all()
    serializer = CargoSerializer(cargo, many=True)
    response = serializer.data
    message = "Cargo list retrieved successfully." if response else "No cargo found."

    return custom_response(response, status, message)

@api_view(['PUT'])
def update_cargo(request, id):
    response = []
    status = 200
    message = ""


    
    cargo = Cargo.objects.filter(id=id).first()
    if not cargo:
        message = "Cargo not found."
        return custom_response(response, status, message)

    data = request.data
    allowed_fields = {"type", "description"}
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
    serializer = CargoSerializer(cargo, data=filtered_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response = serializer.data
        message = "Cargo updated successfully."
    else:
        response = serializer.errors
        status = 400
        message = "Validation failed."

    return custom_response(response, status, message)

@api_view(['POST'])
def create_booking(request):
    response = []
    status = 200
    message = ""

    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = serializer.data
        message = "Booking created successfully."
    else:
        response = serializer.errors
        status = 400
        message = "Validation failed."

    return custom_response(response, status, message)

@api_view(['GET'])
def list_booking(request):
    response = {}
    status = 200
    message = ""

    # Get pagination parameters from query params
    page = int(request.GET.get('page', 1))  # Default page is 1
    per_page = int(request.GET.get('per_page', 10))  # Default per_page is 10

    # Implementing pagination
    paginator = PageNumberPagination()
    paginator.page_size = per_page  # Set the page size dynamically

    bookings = Booking.objects.all()

    # Apply pagination
    paginated_bookings = paginator.paginate_queryset(bookings, request)

    if paginated_bookings:
        serializer = BookingDetailSerializer(paginated_bookings, many=True)
        response = {
            'total_items': paginator.page.paginator.count,  # Total items available
            'total_pages': paginator.page.paginator.num_pages,  # Total pages
            'current_page': page,  # Current page
            'per_page': per_page,  # Items per page
            'data': serializer.data  # The actual paginated data
        }
        message = "Booking list retrieved successfully."
    else:
        message = "No bookings found."

    return custom_response(response, status, message)

@api_view(['GET'])
def booking_detail(request, id):
    response = []
    status = 200
    message = ""

    booking = Booking.objects.filter(id=id).first()
    if booking:
        serializer = BookingSerializer(booking)
        response = serializer.data
        message = "Booking details retrieved successfully."
    else:
        message = "Booking not found."

    return custom_response(response, status, message)

@api_view(['PUT'])
def update_booking(request, id):
    response = []
    status = 200
    message = ""

    booking = Booking.objects.filter(id=id).first()
    if not booking:
        message = "Booking not found."
        return custom_response(response, status, message)

    serializer = BookingSerializer(booking, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response = serializer.data
        message = "Booking updated successfully."
    else:
        response = serializer.errors
        status = 400
        message = "Validation failed."

    return custom_response(response, status, message)
