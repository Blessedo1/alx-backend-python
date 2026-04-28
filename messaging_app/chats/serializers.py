from rest_framework import serializers
from .models import user, Message, Conversation

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ["user_id", "first_name", "last_name", "email", "phone_number", "role", "created_at"]
        read_only_fields = ["user_id", "created_at"]

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants_id", "created_at"]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["message_id", "sender", "conversation", "message_body", "sent_at"]
