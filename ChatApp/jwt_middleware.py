import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from ChatApp import settings

@database_sync_to_async
def get_user(validated_token):
    """function to get user details from the validated token using asynchronous database access.

    Args:
        validated_token (_type_): JWT Token

    Returns:
        _type_: coroutine object(userObject or anonymousUserObject)
    """
    try:
        payload = jwt.decode(validated_token, settings.SECRET_KEY,algorithms="HS256")
        user = get_user_model()
        user = user.objects.get(user_id=payload['user_id'])
        return user
    except:
        return AnonymousUser()

class JwtAuthMiddleware(BaseMiddleware):
    """Middleware class that implements the JWT authentication mechanism.
    """
    def __init__(self, inner):
        """
        Args:
            inner: The purpose of this argument is to chain the middleware and pass the request to the next middleware in the stack for further processing.
        """
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """ This method retrieves the token from the query parameters in the scope dictionary 
            and calls the get_user() function to validate the token and retrieve the user object. 
            It then sets the user attribute in the scope dictionary to the retrieved user object. 
            Finally, the method calls the __call__() method of the super() class to pass the request to the next middleware in the stack for further processing.

        Args:
            scope: Dictionary that contains information about the current WebSocket connection, including the WebSocket path, query parameters, headers.
            receive: Coroutine function that is used to receive messages from the WebSocket connection.
            send: Coroutine function that is used to send messages to the WebSocket connection.
        """
        query = dict((x.split("=") for x in scope["query_string"].decode().split("&")))
        scope["user"] = await get_user(validated_token=query.get('token'))
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    """function that returns an instance of the JwtAuthMiddleware class.
    """
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))