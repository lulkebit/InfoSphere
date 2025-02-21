from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'title', 'content', 'created_at', 'updated_at', 
            'is_read', 'priority', 'source_name', 'author', 'url', 
            'image_url', 'published_at', 'category'
        ]
        read_only_fields = ['created_at', 'updated_at', 'published_at'] 