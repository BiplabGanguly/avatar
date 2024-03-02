from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.urls import reverse


class AuthSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'
    
    def post(self, req,*args, **kwargs):
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(req,user)
            dashboard_url = reverse('dashboards:index', kwargs={'uid': user.id})
            return redirect(dashboard_url)
        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context
