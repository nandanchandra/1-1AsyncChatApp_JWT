from django.urls import path
from api.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/message/<uuid:user_id>', ChatConsumer.as_asgi()),
]