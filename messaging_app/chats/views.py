from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    ConversationListSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from rest_framework import authentication, permissions
from rest_framework import action

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Users can only access conversations they participate in..
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer
    def get_queryset(self):
        """
        Return only conversations where the current user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    Users can only access messages from conversations they participate in.
    Implements pagination (20 messages per page) and filtering.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer
    def get_queryset(self):
        """
        Return messages from conversations where the current user is a participant.
        """
        user_conversations = Conversation.objects.filter(
            participants=self.request.user
        )
        return Message.objects.filter(
            conversation__in=user_conversations
        ).order_by('-sent_at')
