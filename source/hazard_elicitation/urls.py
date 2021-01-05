from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('archex/', include('archex_backend.urls')),
    path('dialogflow_backend/', include('dialogflow_backend.urls')),
]
