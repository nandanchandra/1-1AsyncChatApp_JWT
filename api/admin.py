from django.contrib import admin
from .models import ChatMessage, Thread
# Register your models here.

class ThreadAdmin(admin.ModelAdmin):
    list_display = ("user_one","user_two",)

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user",)

admin.site.register(Thread,ThreadAdmin)
admin.site.register(ChatMessage,ChatMessageAdmin)