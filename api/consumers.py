import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import User
from api.models import ChatMessage, Thread

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
            This function is called when a new websocket connection is established. It accepts the connection,
            retrieves the user object and other user's ID from the URL route parameters, gets the 
            user object, gets the chat thread object for the current user and the other user, sets the name of
            the room group to the chat thread's group name, and adds the channel to the room group.
        """
    
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
        """
            This function is called when a message is received from the websocket. It extracts the message
            from the JSON payload, saves the message to the database, and sends the message to the room group.
        """

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
        """
            This function is called when the websocket connection is closed and 
            ensure that the channel is removed from the room group when the connection is closed.
        """
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    async def chat_message(self, event):
        """
            This function is called when a message is sent to the room group. It sends the message to the client
            that initiated the websocket connection, along with a flag indicating whether the message is from the
            client or from the other user in the chat.
        """
        is_self = str(self.scope['user'].user_id) == event['from'] 
        await self.send(text_data=json.dumps({
            "type": "websocket.send",
            "text": event['message'],
            "self" : is_self
        }))

    @database_sync_to_async    
    def get_other_user(self, other_user_id):
        """
            This function retrieves the user object for the given user ID asynchronously from the database.
        """
        return User.objects.get(user_id= other_user_id)

    @database_sync_to_async
    def get_thread(self, user, other_user):
        """
            This function retrieves the chat thread object for the given user and other user asynchronously
            from the database. If the chat thread does not exist, it creates a new one.
        """
        return Thread.objects.get_or_new(user, other_user)

    @database_sync_to_async
    def save_chat(self, message):
        """
            This function saves the chat message to the database asynchronously.
        """
        ChatMessage.objects.create(thread=self.thread, message=message, user=self.scope['user'])