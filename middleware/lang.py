from django.utils.translation import activate
from auth.models import Profile
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist exception

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Retrieve the language from the database for the current user
                user_profile = Profile.objects.get(user=request.user)
                user_language = user_profile.user_language  # Update attribute name

                # Activate the user's language for this request
                print('language:::::::::::::', user_language)
                if user_language:
                    activate(user_language)
            except ObjectDoesNotExist:
                # Handle the case where no Profile object is found for the user
                # You can use a default language or handle the case as appropriate for your application
                pass

        response = self.get_response(request)
        return response
