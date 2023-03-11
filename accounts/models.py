import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class UserAccountManager(BaseUserManager):

    def create_user(self , email , name="Anonymous",password = None):
            if not email or len(email) <= 0 :
                raise  ValueError("Email field is required !")
            if not password :
                raise ValueError("Password is must !")
            user = self.model(email = self.normalize_email(email),name=name)
            user.set_password(password)
            user.save(using = self._db)
            return user
            
    def create_superuser(self , email , password):
        user = self.create_user(email = self.normalize_email(email) ,password = password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
    
class User(AbstractBaseUser):

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=254, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects=UserAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self , perm, obj = None):
        return self.is_admin

    def has_module_perms(self , app_label):
        return True