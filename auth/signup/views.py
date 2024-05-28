from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.contrib.auth.models import User
import logging
from auth.models import Profile

# log...........................
logger = logging.getLogger('main')


class AuthSignupView(TemplateView):
    template_name = 'pages/auth/signup.html'
    
    def post(self, req, *args, **kwargs):
        try:
            email = req.POST['email']
            username = req.POST['username']
            password = req.POST['password']
            confirm_password = req.POST['confirm-password']
            
            if password == confirm_password and password != "":
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                logger.info('User signed up successfully: {}'.format(username))
                return redirect('/signin/')
            else:
                logger.warning('Passwords do not match or are empty for user: {}'.format(username))
                return redirect('signup/')
        except Exception as e:
            logger.error('An error occurred during user signup: {}'.format(str(e)))
            return redirect('signup/')
            

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context = KTLayout.init(context)
            KTTheme.addJavascriptFile('js/custom/authentication/sign-up/general.js')
            context.update({
                'layout': KTTheme.setLayout('auth.html', context),
            })
            logger.info('Context data retrieved successfully for sign-up page')
        except Exception as e:
            logger.error('An error occurred while retrieving context data for sign-up page: {}'.format(str(e)))
        return context
