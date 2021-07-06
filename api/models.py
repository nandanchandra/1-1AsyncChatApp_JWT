from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class ThreadManager(models.Manager):

    def get_or_new(self, user, other_user): # get_or_create
        if user == other_user:
            return None, False
        qlookup1 = Q(user_one=user) & Q(user_two=other_user)
        qlookup2 = Q(user_one=other_user) & Q(user_two=user)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            if user != other_user:
                obj = self.model(user_one=user, user_two=other_user)
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_first')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    
    @property
    def room_group_name(self):
        return f'chat_{self.id}'


class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)