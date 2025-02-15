from django.http import JsonResponse

class JsonErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            if hasattr(response, 'data') and response.data:
                return JsonResponse({
                    "status": response.data.get('status'),
                    "status_code": response.data.get('status_code'),
                    "message": response.data.get('message'),
                    "response": response.data.get('response')
                }, status=response.status_code)
            else:
                return JsonResponse({
                    "status": "failed",
                    "status_code": 404,
                    "message": "The requested resource was not found.",
                    "response": {}
                }, status=404)


        return response
