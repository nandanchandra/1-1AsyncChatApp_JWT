from django.urls import path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/message/<int:id>', ChatConsumer.as_asgi()),
]