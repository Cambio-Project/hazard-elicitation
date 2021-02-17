from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from architecture_extraction_backend.models import ArchitectureModelViewSet
from . import views


router = routers.DefaultRouter()
router.register(r'architecture_models', ArchitectureModelViewSet, basename='architecture_models')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('archex/', include('architecture_extraction_backend.urls')),
    path('dialogflow_backend/', include('dialogflow_backend.urls')),

    path('', views.ui),
    path('ui/', views.ui),
    path('upload/', views.upload),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
