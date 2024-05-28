from django.views.generic import TemplateView
from django.shortcuts import redirect,render
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from . import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import openai
from dashboards.apidata import api
# import datetime
import logging
# from django.utils import timezone
# import pytz
from auth.models import Profile

#logger.............
logger = logging.getLogger('main')
# now = datetime.datetime.now()
# current_timezone = now.astimezone().tzinfo

openai.api_key = api

class DashboardsView(TemplateView):
    template_name = 'pages/dashboards/index.html'
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context = KTLayout.init(context)
            KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
           
            # current_datetime = timezone.now()
            # timezone_obj = pytz.timezone(settings.TIME_ZONE)
            # current_datetime_timezone = current_datetime.astimezone(timezone_obj)
            
            profile = Profile.objects.get(user_id = self.kwargs['uid'])
            print(profile.created_at)
            scripts_data = models.Scripts.objects.filter(user_id=self.kwargs['uid'], is_delete=False)
            # zone_data = Profile.objects.get(user_id = self.kwargs['uid'])
            context['data'] = scripts_data
            self.request.session['uid'] = self.kwargs['uid']
            user = User.objects.get(id=self.kwargs['uid'])
            context['user'] = user
            context['datetime'] = profile.created_at
            
            logger.info('Context data retrieved successfully for dashboards page')
        except Exception as e:
            logger.error('An error occurred while retrieving context data for dashboards page: {}'.format(str(e)))
        return context
    
    


class ScriptView(TemplateView):
    template_name = 'pages/dashboards/scripts.html'
    
    def get_context_data(self, **kwargs):
        try:
            # Your existing code to retrieve context data
            script = models.Scripts.objects.get(id=self.kwargs['sid'])
            context = super().get_context_data(**kwargs)
            context = KTLayout.init(context)
            context['content'] = script.script
            self.request.session['sid'] = self.kwargs['sid']
            context['sid'] = self.kwargs['sid']
            context['scriptitlt'] = script.title
            uid = self.request.session['uid']
            user = User.objects.get(id=uid)
            KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
            
            # Log an info message indicating successful retrieval of context data
            logger.info('Context data retrieved successfully for the view.')

        except Exception as e:
            # Log an error message if an exception occurs during context data retrieval
            logger.error('An error occurred while retrieving context data: %s', e, exc_info=True)

        # Return the context
        return context
        
    
        
class PostScriptView(TemplateView):
    template_name = 'pages/dashboards/scripts.html'
    
    def post(self, request, *args, **kwargs):
        user_id=self.kwargs['uid']
        try:
            script_type = request.POST.get('script_type')
            title = request.POST.get('script_title')
            plot = request.POST.get('plot')
            genre = request.POST.get('script_genre')
            synopsis = request.POST.get('synopsis')
            social_plat = request.POST.get('social_platform')

            if script_type == "feature film":
                script_feature = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "Generate an engaging script for feature film"},
                        {"role": "user", "content": f"film title: {title}"},
                        {"role": "user", "content": f"film genre: {genre}"},
                        {"role": "user", "content": f"film synopsis: {synopsis}"},
                        {"role": "user", "content": f"plot of the film: {plot}"}
                    ]
                )
                content = script_feature['choices'][0]['message']['content'].strip()
                script = models.Scripts(
                    title=title,
                    script=content,
                    user_id=self.kwargs['uid'],
                    script_type=script_type,
                    script_genre=genre)
                script.save()
                logger.info('Script saved successfully for feature film type.')
                return redirect('dashboards:scripts', script.id)
            else:
                script_short = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "Generate a short and engaging script for a video"},
                        {"role": "user", "content": f"title of the video: {title}"},
                        {"role": "user", "content": f"social platform: {social_plat}"},
                        {"role": "user", "content": f"plot of the script: {plot}"}
                    ]
                )
                content = script_short['choices'][0]['message']['content'].strip()
                script = models.Scripts(
                    title=title,
                    script=content,
                    script_type=script_type,
                    platform=social_plat)
                script.save()
                logger.info('Script saved successfully for short video type.')
                return redirect('dashboards:scripts', script.id)
        except Exception as e:
            # Log an error message if an exception occurs
            logger.critical('An error occurred while processing the script: %s', e, exc_info=True)
            # Redirect to an error page or display an error message to the user
            return redirect('dashboards:index',user_id)

        
    
    


class editScript(TemplateView):
    def post(self, req, *args, **kwargs):
        sid = self.kwargs['sid']
        try:
            script = req.POST.get('script')
            models.Scripts.objects.filter(id=self.kwargs['sid']).update(script=script)
            logger.info('Script updated successfully')
        except Exception as e:
            logger.error('An error occurred while updating the script: %s', e, exc_info=True)
        return redirect('dashboards:scripts', sid)
        
        
class editCopilotScript(TemplateView):
    def post(self, req, *args, **kwargs):
        sid = self.kwargs['sid']  # Define sid before the try block
        try:
            copilot_plot = req.POST.get('copilot_plot')
            script = models.Scripts.objects.get(id=sid)
            copilot_script = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "complete the paragraph"},
                    {"role": "user", "content": f"next plot : {copilot_plot}"}
                ]
            )
            recent_script = copilot_script['choices'][0]['message']['content'].strip()
            modified_script = script.script.replace(copilot_plot, recent_script)
            models.Scripts.objects.filter(id=sid).update(script=modified_script)
            logger.info('Script updated with Copilot assistance successfully')
        except Exception as e:
            logger.error('An error occurred while updating the script with Copilot assistance: %s', e, exc_info=True)
        return redirect('dashboards:scripts', sid)
        
        
        
class deleteScript(TemplateView):
   def post(self, req, *args, **kwargs):
        try:
            sid = self.kwargs['sid']
            models.Scripts.objects.filter(id=sid).update(is_delete=True)
            uid = self.request.session['uid']
            logger.info('Script with id %s deleted successfully', sid)
        except Exception as e:
            logger.error('An error occurred while deleting the script with id %s: %s', sid, e, exc_info=True)
        return redirect('dashboards:index', uid)


def changeTimeZone(request, uid):
    if request.method == "POST":
        selected_timezone = request.POST.get('selectedTimezone')
        if selected_timezone:
            # Update the user's profile with the selected timezone
            profile = Profile.objects.get(user_id=uid)
            profile.user_timezone = selected_timezone
            profile.save()

            # Update the session with the selected timezone
            request.session['user_timezone'] = selected_timezone

            return redirect('dashboards:index', uid=uid)
        
        
def change_language(req, uid):
    if req.method == "POST":
        select_language = req.POST.get('select_language')
        if select_language:
            profile = Profile.objects.get(user_id=uid)
            profile.user_language = select_language
            profile.save()
            req.session['user_language'] = select_language
            # Generate the URL for the 'index' pattern with the uid parameter
            new_url = reverse('dashboards:index', kwargs={'uid': uid})
            new_url = '/' + select_language + new_url[3:] 
            return redirect(new_url)



  
    

    

