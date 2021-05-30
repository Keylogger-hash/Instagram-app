"""
ASGI config for instagram project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram.settings')

application = ProtocolTypeRouter({
      "http":get_asgi_application(),
      "websocket":AuthMiddlewareStack(
      URLRouter(
      websocket_urlpatterns
      )
   ),
})
#channel_layer = channels.asgi.get_channel_layer()
