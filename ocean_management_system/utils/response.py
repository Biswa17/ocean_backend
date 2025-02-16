from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    APIException, AuthenticationFailed, NotAuthenticated, 
    PermissionDenied, ValidationError
)
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
import logging

# Set up logging for debugging purposes
logger = logging.getLogger(__name__)

def custom_response(data=None, status=200, message=""):
    """
    Standardized API response format for Django REST Framework.

    :param data: The response data (default: None)
    :param status: HTTP status code (default: 200)
    :param message: Custom message (default: empty string)
    :return: Response object in a uniform structure
    """

    # Default response structure

    is_success = status in [200, 201, 202, 203, 204]
    response = {
        "status": "success" if is_success else "failed",
        "status_code": status,
        "message": message or get_default_message(status),
        "response": data if data is not None else {}
    }

    # Handling error cases
    if status >= 400:
        response["response"] = {"errors": data or "An error occurred."}

    return Response(response, status=status)


def get_default_message(status):
    """
    Returns a default message based on HTTP status code.
    """
    messages = {
        drf_status.HTTP_200_OK: "Request successful.",
        drf_status.HTTP_201_CREATED: "Resource created successfully.",
        drf_status.HTTP_400_BAD_REQUEST: "Bad request. Please check your input.",
        drf_status.HTTP_401_UNAUTHORIZED: "Authentication required.",
        drf_status.HTTP_403_FORBIDDEN: "Access denied.",
        drf_status.HTTP_404_NOT_FOUND: "Requested resource not found.",
        drf_status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error. Try again later.",
    }
    return messages.get(status, "An unexpected error occurred.")


def custom_exception_handler(exc, context):
    """Handles all exceptions globally and returns a standardized custom response."""
    
    # First, let DRF handle its built-in exceptions
    response = exception_handler(exc, context)

    # Extract useful information for debugging
    error_message = str(exc)
    view_name = context['view'].__class__.__name__ if 'view' in context else 'UnknownView'
    request_path = context['request'].path if 'request' in context else 'UnknownPath'
    
    logger.error(f"Exception in {view_name} at {request_path}: {error_message}")

    if response is not None:
        # Handle specific DRF exceptions
        # Authentication Errors (401)
        if isinstance(exc, NotAuthenticated):
            return custom_response(data={}, status=401, message="Missing authentication token")

        elif isinstance(exc, AuthenticationFailed):
            return custom_response(data={}, status=401, message="Token is invalid or expired")
            

        if isinstance(exc, PermissionDenied):
            return custom_response(data={}, status=403, message="You do not have permission to perform this action")

        if isinstance(exc, ValidationError):
            return custom_response(data=exc.detail, status=400, message="Validation failed")

    else:
        # Handle non-DRF exceptions (database errors, unexpected errors)
        if isinstance(exc, DatabaseError):
            return custom_response(data={}, status=500, message="A database error occurred")

        if isinstance(exc, ObjectDoesNotExist):
            return custom_response(data={}, status=404, message="The requested resource was not found")

        # Handle any other unhandled exceptions
        return custom_response(data={}, status=500, message="An unexpected error occurred. Please try again later")

    return response  # Return default DRF response if no custom handling is needed


def has_permission(user, instance):
    """
    Generic permission checker for model updates.
    - Allows update if the user is an admin.
    - Allows update if the user owns the instance (has a `user` field).
    """
    if user.is_admin:
        return True

    if hasattr(instance, "user"):
        return instance.user == user

    return False  # Deny update if `user` field does not exist
