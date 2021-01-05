from django.urls import re_path

from dialogflow_backend.websocket.df_websocket import DFWebsocket

url_patterns = [
    re_path(r'^ws/df/$', DFWebsocket.as_asgi())
]
