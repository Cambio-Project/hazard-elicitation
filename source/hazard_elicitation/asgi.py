import os

import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hazard_elicitation.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
import dialogflow_backend.routing

application = ProtocolTypeRouter({
    "http":      get_asgi_application(),
    "websocket": URLRouter(
        dialogflow_backend.routing.url_patterns
    ),
})
