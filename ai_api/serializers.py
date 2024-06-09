from rest_framework import serializers
from .models import *

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'start_time']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'query', 'answer','chat_type']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Files_data
        fields=['id','file']