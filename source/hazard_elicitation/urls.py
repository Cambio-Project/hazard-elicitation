from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers

from software_architecture_extraction.source.extractor.models.architecture import ArchitectureModelViewSet, ArchitectureModelListViewSet
from . import views


router = routers.DefaultRouter()
router.register(r'arch', ArchitectureModelViewSet, basename='arch')
router.register(r'archlist', ArchitectureModelListViewSet, basename='archlist')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/img/hazard.png', permanent=True)),

    path('archex/', include('software_architecture_extraction.source.extractor.urls')),
    path('df/', include('dialogflow_backend.urls')),

    path('', views.ui),
    path('ui/', views.ui),
    path('upload/', views.upload),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
