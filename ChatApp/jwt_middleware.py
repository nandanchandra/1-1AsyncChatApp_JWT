import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(validated_token):
    try:
        settings.configure()
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