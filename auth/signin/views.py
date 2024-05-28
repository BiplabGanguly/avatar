from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login,logout
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.urls import reverse
import datetime
import logging
import pytz
from django.utils import timezone
from auth.models import Profile


#logger......................
logger = logging.getLogger('main')
now = datetime.datetime.now()
current_timezone = now.astimezone().tzinfo



class AuthSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'

    def post(self, req, *args, **kwargs):
        username = req.POST.get('username')
        password = req.POST.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Login the user
            login(req, user)
            # Redirect to the dashboard page
            logger.info('login username: %s', username)
        
            req.session['uid'] = user.id
            profile = Profile.objects.get(user_id=user.id)
            
            new_url = reverse('dashboards:index', kwargs={'uid': user.id})
            new_url = '/' + profile.user_language + new_url[3:] 

            return redirect(new_url)
        else:
            # Log unsuccessful login attempts
            logger.warning('Failed login attempt for username: %s', username)

            # Redirect to the signin page
            return redirect('/signin/')
        
        

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context = KTLayout.init(context)
            KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')
            context.update({
                'layout': KTTheme.setLayout('auth.html', context),
            })
            logger.info('Retrieving context data')

        except Exception as e:
            logger.exception("An error occurred while retrieving context data:")
        return context
    
    
def log_out(req):
    # Perform logout
    logout(req)
    # Log an INFO message
    logger.info('User logged out successfully')
    # Redirect to the home page
    return redirect('auth:home')


def home_page(req):
    try:       
        return render(req, 'pages/auth/home.html')
    except Exception as e:
        # Log the exception at the appropriate level
        logger.exception("An error occurred while rendering the home page:")
        # Optionally, you can redirect to an error page or handle the error in another way
        return HttpResponse("An error occurred while rendering the home page. Please try again later.")