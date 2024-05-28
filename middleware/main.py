from django.utils import timezone
from auth.models import Profile
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist exception

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Retrieve the timezone from the database for the current user
                user_profile = Profile.objects.get(user=request.user)
                user_timezone = user_profile.user_timezone  # Update attribute name

                # Activate the user's timezone for this request
                print('timezone:::::::::::::',user_timezone)
                if user_timezone:
                    timezone.activate(user_timezone)
            except ObjectDoesNotExist:
                # Handle the case where no Profile object is found for the user
                # You can use a default timezone or handle the case as appropriate for your application
                pass

        response = self.get_response(request)
        return response
