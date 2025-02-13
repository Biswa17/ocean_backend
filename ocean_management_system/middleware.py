from django.http import JsonResponse

class JsonErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return JsonResponse({
                "status": "failed",
                "status_code": 404,
                "message": "The requested resource was not found.",
                "response": {}
            }, status=404)

        return response
