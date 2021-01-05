from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path('test/', views.test),
    path('bot/', views.bot),
    path('dialogflow-webhook/', csrf_exempt(views.dialogflow_webhook))
]
