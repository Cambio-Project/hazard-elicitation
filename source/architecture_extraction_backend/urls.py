from django.urls import path
from django.views.decorators.csrf import csrf_exempt

import architecture_extraction_backend.views as views

urlpatterns = [
    path('upload/', csrf_exempt(views.upload))
]
