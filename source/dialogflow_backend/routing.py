from django.urls import re_path

from dialogflow_backend.dialogflow.websocket import DFWebsocket

url_patterns = [
    re_path(r'^ws/df/$', DFWebsocket.as_asgi())
]
