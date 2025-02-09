from rest_framework.response import Response
from rest_framework import status as drf_status

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
