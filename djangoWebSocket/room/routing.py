from django.urls import re_path
from . import RoomConsumer
from game import consumers
websocket_urlpatterns = [
    re_path(r'ws/room/', RoomConsumer.RoomConsumer.as_asgi()),
    re_path(r'ws/game/', consumers.PongConsumer.as_asgi())
]