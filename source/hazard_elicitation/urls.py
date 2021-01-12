from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('archex/', include('architecture_extraction_backend.urls')),
    path('dialogflow_backend/', include('dialogflow_backend.urls')),

    path('ui/', views.ui),
]
