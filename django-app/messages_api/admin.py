from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_read', 'priority')
    list_filter = ('is_read', 'priority', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
