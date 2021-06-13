from django.urls import re_path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
   re_path(r'^ws/chat/(?P<label>[^/]+)/',ChatConsumer.as_asgi())
]
