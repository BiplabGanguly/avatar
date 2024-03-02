from django.urls import path
from django.conf import settings
from dashboards.views import DashboardsView, ScriptView
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'dashboards'

urlpatterns = [
    path('dashboard/<uid>/', login_required(DashboardsView.as_view()), name='index'),

    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
    path('script/<sid>/', login_required(ScriptView.as_view()),name="scripts"),
    path('post_script/<uid>',login_required(views.PostScriptView.as_view()),name="post_script"),
    path('edit_script/<sid>/',login_required(views.editScript.as_view()),name='edit_script'),
    path('edit_copilot/<sid>/',login_required(views.editCopilotScript.as_view()),name='edit_copilot'),

]