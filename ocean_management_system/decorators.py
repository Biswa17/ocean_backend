from functools import wraps
from django.http import JsonResponse

def user_filter_decorator(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({"message": "Authentication required"}, status=401)

        # Admin can pass `user_id`, others default to their own ID
        request.user_filter_id = request.GET.get("user_id") if user.is_admin else user.id

        return view_func(request, *args, **kwargs)

    return wrapper
