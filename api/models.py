from django.db import models
from accounts.models import User
from api.manager import ThreadManager

class Thread(models.Model):
    """Represents a chat thread between two users.
    """
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_first')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    
    @property
    def room_group_name(self):
        return f'chat_{self.id}'

class ChatMessage(models.Model):
    """Represents a chat message sent by a user in a chat thread.
    """
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)