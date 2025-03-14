from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cargo, Container
from .serializers import CargoSerializer, ContainerSerializer
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
def create_container(request):
    response = []
    status = 200
    message = ""

    serializer = ContainerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = serializer.data
        message = "Container created successfully."
    else:
        response = serializer.errors
        status = 400
        message = "Validation failed."

    return custom_response(response, status, message)

@api_view(['GET'])
def list_containers(request):
    response = []
    status = 200
    message = ""

    containers = Container.objects.all()
    serializer = ContainerSerializer(containers, many=True)
    response = serializer.data
    message = "Container list retrieved successfully." if response else "No containers found."

    return custom_response(response, status, message)

@api_view(['PUT'])
def update_container(request, id):
    response = []
    status = 200
    message = ""

    container = Container.objects.filter(id=id).first()
    if not container:
        message = "Container not found."
        return custom_response(response, 404, message)

    serializer = ContainerSerializer(container, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response = serializer.data
        message = "Container updated successfully."
    else:
        response = serializer.errors
        status = 400
        message = "Validation failed."

    return custom_response(response, status, message)
