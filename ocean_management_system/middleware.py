from django.http import JsonResponse

class JsonErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)# Skip middleware for specific paths (e.g., API paths)
        if request.path.startswith('/api/'):
            # Check if the response status code is not successful (other than 2xx)
            if response.status_code == 404:
                response_data = {
                    "status": response.data.get('status'),
                    "status_code": response.data.get('status_code'),
                    "message": response.data.get('message'),
                    "response": response.data.get('response')
                }
                return JsonResponse(response_data, status=response.status_code)


        if response.status_code == 404:
            return JsonResponse({
                "status": "failed",
                "status_code": 404,
                "message": "The requested resource was not found.",
                "response": {}
            }, status=404)

        return response
