from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from . import models
from django.contrib.auth.models import User
import openai

openai.api_key = "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"



class DashboardsView(TemplateView):
    template_name = 'pages/dashboards/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        print(kwargs)
        scripts_data = models.Scripts.objects.filter(user_id = self.kwargs['uid'], is_delete = False)
        context['data']  = scripts_data
        self.request.session['uid'] = self.kwargs['uid']
        user = User.objects.get(id = self.kwargs['uid'])
        context['user'] = user
        return context
    
    


class ScriptView(TemplateView):
    template_name = 'pages/dashboards/scripts.html'
    
    def get_context_data(self, **kwargs):
        script = models.Scripts.objects.get(id = self.kwargs['sid'])
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['content'] = script.script
        self.request.session['sid'] = self.kwargs['sid']
        context['sid'] = self.kwargs['sid']
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        return context
        
    
        
class PostScriptView(TemplateView):
    template_name = 'pages/dashboards/scripts.html'
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('script_title')
        genre = request.POST.get('genre')
        plot = request.POST.get('script_plot')

        script = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                    {"role" : "user" , "content" : "create a drama script" },
                    {"role" : "user" , "content" :  f"title: {title}"},
                    {"role" : "user" , "content" :  f"gonre : {genre}"},
                    {"role" : "user" , "content" :  f"plot : {plot}"}
            ]
        )
        content = script['choices'][0]['message']['content'].strip()
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['content'] = content
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        script = models.Scripts(title = title, script = content, user_id = self.kwargs['uid'])
        script.save()
        context['sid'] = script.id
        print(script.id)
        return render(request, self.template_name,context)
    
    


class editScript(TemplateView):
    def post(self, req, *args, **kwargs):
        script = req.POST.get('script')
        models.Scripts.objects.filter(id=self.kwargs['sid']).update(script = script)
        sid =   self.kwargs['sid'] 
        return redirect('dashboards:scripts',sid)
        
        
    

class editCopilotScript(TemplateView):
    def post(self, req, *args, **kwargs):
        copilot_plot = req.POST.get('copilot_plot')
        previous_script = models.Scripts.objects.get(id = self.kwargs['sid'])
        copilot_script = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                    {"role" : "user" , "content" : "extend the drama script" },
                    {"role" : "user" , "content" :  f"next plot : {copilot_plot}"}
            ]
        )
        recent_script = copilot_script['choices'][0]['message']['content'].strip()
        main_script = previous_script.script + recent_script
        models.Scripts.objects.filter(id = self.kwargs['sid']).update(script = main_script)
        sid = self.kwargs['sid']
        return redirect('dashboards:scripts',sid)
        


  
    

