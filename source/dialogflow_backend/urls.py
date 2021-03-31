from django.urls import path

import dialogflow_backend.views as views


urlpatterns = [
    path('detect_intent', views.detect_intent),
    path('detect_event', views.detect_event),
    path('export_study', views.export_study)
]
