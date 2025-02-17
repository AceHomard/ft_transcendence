from django.urls import re_path
from . import Consumer

websocket_urlpatterns = [
    re_path(r'ws/notif/', Consumer.Consumer.as_asgi())
]
