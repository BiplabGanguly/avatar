from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.contrib.auth.models import User

class AuthSignupView(TemplateView):
    template_name = 'pages/auth/signup.html'
    
    def post(self, req, *args, **kwargs):
        email = req.POST['email']
        username = req.POST['username']
        password = req.POST['password']
        confirm_password = req.POST['confirm-password']
        
        if(password == confirm_password and password != ""):
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('/')
        return redirect('signup/')
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('js/custom/authentication/sign-up/general.js')
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context
