import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import User
from api.models import ChatMessage, Thread

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_anonymous:
            await self.accept()
            user = self.scope['user']
            other_user_id = self.scope['url_route']['kwargs']['user_id']
            other_user = await self.get_other_user(other_user_id)

            self.thread, _ = await self.get_thread(user, other_user)

            self.room_group_name = self.thread.room_group_name
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.save_chat(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                "from" : str(self.scope['user'].user_id)

            }
        )

    async def disconnect(self, close_code):
        pass

    async def chat_message(self, event):
        is_self = str(self.scope['user'].user_id) == event['from'] 
        await self.send(text_data=json.dumps({
            "type": "websocket.send",
            "text": event['message'],
            "self" : is_self
        }))

    @database_sync_to_async    
    def get_other_user(self, other_user_id):
        return User.objects.get(user_id= other_user_id)

    @database_sync_to_async
    def get_thread(self, user, other_user):
        return Thread.objects.get_or_new(user, other_user)

    @database_sync_to_async
    def save_chat(self, message):
        ChatMessage.objects.create(thread=self.thread, message=message, user=self.scope['user'])