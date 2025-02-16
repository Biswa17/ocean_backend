from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking, Tracking
from cargo.models import Cargo
from .serializers import CargoSerializer, BookingSerializer,BookingDetailSerializer,TrackingSerializer
from ocean_management_system.utils.response import custom_response
from rest_framework.pagination import PageNumberPagination




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

    # Get user_id filter (optional)
    user_id = request.GET.get('user_id', None)

    bookings = Booking.objects.all()

    # Apply user_id filter if provided
    if user_id:
        bookings = bookings.filter(user_id=user_id)

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
        serializer = BookingDetailSerializer(booking)
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


@api_view(['POST'])
def create_tracking(request):
    response = []
    status = 200
    message = ""

    try:
        data = request.data  # No need for JSONParser
        booking_id = data.get("booking_id")

        # Validate booking_id
        if not booking_id:
            message = "Booking ID is required"
            status = 404
            return custom_response(response, status, message)

        # Check if the booking exists
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking:
            message = "Booking not found"
            status = 404
            return custom_response(response, status, message)

        # Use serializer for validation and creation
        serializer = TrackingSerializer(data=data)
        if serializer.is_valid():
            tracking = serializer.save()  # Creates tracking instance

            # Link tracking to booking
            booking.tracking = tracking
            booking.save()

            response = serializer.data
            message = "Tracking created successfully"
        else:
            status = 400
            message = serializer.errors

    except Exception as e:
        status = 500
        message = f"Error: {str(e)}"

    return custom_response(response, status, message)


@api_view(['GET'])
def get_tracking_details(request, id):
    response = []
    status = 200
    message = ""

    try:
        # Fetch tracking object
        tracking = Tracking.objects.filter(id=id).first()
        
        if not tracking:
            message = "Tracking details not found"
            return custom_response(response, status, message)

        # Serialize and return data
        serializer = TrackingSerializer(tracking)
        response = serializer.data
        message = "Tracking details retrieved successfully"

    except Exception as e:
        status = 500
        message = f"Error: {str(e)}"

    return custom_response(response, status, message)