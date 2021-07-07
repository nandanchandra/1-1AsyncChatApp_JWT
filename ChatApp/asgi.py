import os
import jwt


from django.core.asgi import get_asgi_application
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


from channels.routing import ProtocolTypeRouter, URLRouter


from ChatApp import settings
import api.routing


@database_sync_to_async
def get_user(validated_token):
    try:
        payload = jwt.decode(validated_token, settings.SECRET_KEY,algorithms="HS256")
        user = get_user_model()
        user = user.objects.get(user_id=payload['user_id'])
        return user
    except:
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query = dict((x.split("=") for x in scope["query_string"].decode().split("&")))
        scope["user"] = await get_user(validated_token=query.get('token'))
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(
        URLRouter(
            api.routing.websocket_urlpatterns
        )
    ),
})

