from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Booking, Tracking, Document
from cargo.models import Cargo,Container
from ports.models import Lane
from .serializers import  BookingSerializer,BookingDetailSerializer,TrackingSerializer,DocumentSerializer, PortValidationSerializer,BookingListSerializer,BookingTrackingDetailsSerializer
from ocean_management_system.utils.response import custom_response, has_permission
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ocean_management_system.decorators import user_filter_decorator
from cargo.serializers import ContainerSerializer,ContainerPartialValidationSerializer,CargoSerializer
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking_full_info(request):
    response = []
    status = 200
    message = ""

    data = request.data.copy()  # Create a mutable copy of request data
    data['user'] = request.user.id  # Assign the authenticated user's ID
    

    with transaction.atomic():
        # Validate port data
        port_data = data.get('port')
        port_serializer = PortValidationSerializer(data=port_data)
        if not port_serializer.is_valid():
            return custom_response(port_serializer.errors, 400, "Validation failed.")

        # Get lane information from ports
        from_port_id = port_data.get('from_port_id')
        to_port_id = port_data.get('to_port_id')
        try:
            lane = Lane.objects.get(from_port_id=from_port_id, to_port_id=to_port_id)  # Assuming Lane model exists
            data['lane'] = lane.id  # Adding lane ID to the booking data
        except Lane.DoesNotExist:
            return custom_response({"detail": "Invalid lane between the provided ports."}, 400, "Lane not found.")


        # Validate cargo data
        cargo_data = data.get('cargo')  # Extract cargo data
        cargo_serializer = CargoSerializer(data=cargo_data)
        if not cargo_serializer.is_valid():
            return custom_response(cargo_serializer.errors, 400, "Validation failed.")
        
        cargo = cargo_serializer.save()  # Save cargo and get the created object
        data['cargo'] = cargo.id  # Add cargo ID to the data for booking

        

        # Validate container data (multiple containers)
        container_list = data.get('containers')
        for container_data in container_list:
            container_data['cargo'] = cargo.id
            containers_serializer = ContainerSerializer(data=container_data)
            if not containers_serializer.is_valid():
                return custom_response(containers_serializer.errors, 400, "Validation failed.")
            
            containers_serializer.save()
        
        
        

        # Initialize the serializer with the data
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save()
            # Validate the data for documents
            document_list = data.get('documents', [])
            for document_data in document_list:
                document_data['booking'] = booking.id
                document_serializer = DocumentSerializer(data=document_data)
                if not document_serializer.is_valid():
                    return custom_response(document_serializer.errors, 400, "Validation failed.")
            
                document_data = document_serializer.save()

            response = serializer.data
            message = "Booking created successfully."
        else:
            response = serializer.errors
            status = 400
            message = "Validation failed."

            


    
    
    return custom_response(response, status, message)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking_with_id(request):
    response = []
    status = 200
    message = ""

    data = request.data.copy()  # Create a mutable copy of request data
    data['user'] = request.user.id  # Assign the authenticated user's ID

    serializer = BookingSerializer(data=data)
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
@permission_classes([IsAuthenticated])
@user_filter_decorator
def list_booking(request):
    response = {}
    status = 200
    message = ""

    user_id = request.user_filter_id

    # Get pagination parameters from query params
    page = int(request.GET.get('page', 1))  # Default page is 1
    per_page = int(request.GET.get('per_page', 10))  # Default per_page is 10

    # Implementing pagination
    paginator = PageNumberPagination()
    paginator.page_size = per_page  # Set the page size dynamically

    bookings = Booking.objects.all().order_by('-pk')

    # Apply user_id filter if provided
    if user_id:
        bookings = bookings.filter(user_id=user_id)

    # Apply pagination
    paginated_bookings = paginator.paginate_queryset(bookings, request)

    if paginated_bookings:
        serializer = BookingListSerializer(paginated_bookings, many=True)
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
@permission_classes([IsAuthenticated])
def booking_detail(request, id):
    response = []
    status = 200
    message = ""

    booking = Booking.objects.filter(id=id).first()
    if not booking:
        response = []
        status = 404
        message = 'Booking not found.'
        return custom_response(response, status, message)
        
    if not has_permission(request.user, booking):
        return custom_response({}, 403, "You do not have permission to view this booking.")

    if booking:
        serializer = BookingDetailSerializer(booking)
        response = serializer.data
        message = "Booking details retrieved successfully."
    

    return custom_response(response, status, message)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking(request, id):
    response = []
    status = 200
    message = ""

    booking = Booking.objects.filter(id=id).first()
    if not booking:
        message = "Booking not found."
        return custom_response(response, status, message)
    
    # Use the generic permission checker
    if not has_permission(request.user, booking):
        return custom_response({}, 403, "You do not have permission to update this booking.")

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

        # Fetch the booking associated with this tracking ID
        booking = Booking.objects.filter(tracking_id=id).first()
        
        if not booking:
            message = "No booking found for this tracking ID"
            return custom_response(response, status, message)

        

        # Serialize and return data
        serializer = BookingTrackingDetailsSerializer(booking)
        response = serializer.data
        message = "Tracking details retrieved successfully"

    except Exception as e:
        status = 500
        message = f"Error: {str(e)}"

    return custom_response(response, status, message)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dropdown_data(request):
    response = []
    status_code = 200
    message = ""

    try:
        # Fetch dropdown data
        cargo_types = dict(Cargo.CARGO_TYPE_CHOICES)
        container_types = dict(Container.CONTAINER_TYPE_SIZE_CHOICES)
        usage_options = dict(Container.USAGE_OPTIONS)
        document_types = dict(Document.DOCUMENT_TYPE_CHOICES)

        response = {
            "cargo_types": cargo_types,
            "container_types": container_types,
            "usage_options": usage_options,
            "document_types": document_types
        }
        message = "Dropdown data fetched successfully"

    except Exception as e:
        status_code = 500
        message = f"Error: {str(e)}"

    return custom_response(response, status_code, message)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_document_to_booking(request, booking_id):
    # Initialize response, status, and message
    response, status_code, message = [], 200, ""

    try:
        # Validate request data
        serializer = DocumentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(booking_id=booking_id)
            response = serializer.data
            message = "Document added to booking successfully"
            status_code = 201
        else:
            response = serializer.errors
            status_code = 400
            message = "Invalid data"

    except Exception as e:
        response = {}
        status_code = 500
        message = f"Error: {str(e)}"

    return custom_response(response, status_code, message)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def remove_document_from_booking(request, booking_id, document_id):
    # Initialize response, status, and message
    response, status_code, message = [], 200, ""

    try:
        # Fetch the document
        document = Document.objects.filter(id=document_id, booking_id=booking_id).first()

        if not document:
            return custom_response({}, 404, "Document not found")

        # Delete the document
        document.delete()
        message = "Document removed from booking successfully"

    except Exception as e:
        response = {}
        status_code = 500
        message = f"Error: {str(e)}"

    return custom_response(response, status_code, message)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_documents_by_booking(request, booking_id):
    # Initialize response, status, and message
    response, status_code, message = [], 200, ""

    try:
        # Fetch all documents related to the given booking ID
        documents = Document.objects.filter(booking_id=booking_id)

        if not documents.exists():
            return custom_response([], 404, "No documents found for this booking")

        # Serialize the documents
        response = DocumentSerializer(documents, many=True).data
        message = "Documents retrieved successfully"

    except Exception as e:
        response = []
        status_code = 500
        message = f"Error: {str(e)}"

    return custom_response(response, status_code, message)