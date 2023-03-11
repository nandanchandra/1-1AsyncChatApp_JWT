import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings')
django.setup()

import api.routing
from ChatApp.jwt_middleware import JwtAuthMiddlewareStack

"""The application is defined using ProtocolTypeRouter, with two sub-applications: 
    one for handling HTTP requests and another for WebSocket connections. 
    The WebSocket sub-application is wrapped in a JwtAuthMiddlewareStack to authenticate incoming WebSocket connections.
"""
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(
        URLRouter(
            api.routing.websocket_urlpatterns
        )
    ),
})

