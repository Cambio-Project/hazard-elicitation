import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import dialogflow_backend.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hazard_elicitation.settings')
django.setup()

application = ProtocolTypeRouter({
    "http":      get_asgi_application(),
    "websocket": URLRouter(
        dialogflow_backend.routing.url_patterns
    ),
})
