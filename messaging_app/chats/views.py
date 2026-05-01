from rest_framework import viewsets, permissions, status, filters
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
from django_filters.rest_framework import DjangoFilterBackend

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Users can only access conversations they participate in..
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    # Adding filtering support
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['participants__username']

    def get_queryset(self):
        """
        Return only conversations where the current user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Save the conversation and add the creator as a participant
        instance = serializer.save()
        instance.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    Users can only access messages from conversations they participate in.
    Implements pagination (20 messages per page) and filtering.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    # Adding filtering to find messages by content or date
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['text']
    ordering_fields = ['created_at']

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

    def perform_create(self, serializer):
        # Automatically set the sender to the current user
        # This is the "Send Message" implementation
        serializer.save(sender=self.request.user)
