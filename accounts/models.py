
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=50, default='Anonymous')

    email = models.EmailField(max_length=254, unique=True)

    # username = None

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id,self.email