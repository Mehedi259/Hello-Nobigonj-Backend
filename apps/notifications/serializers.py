from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    time = serializers.CharField(source='time_ago', read_only=True)
    type = serializers.CharField(source='notification_type')

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'time', 'read', 'type', 'notification_type', 'created_at']
        read_only_fields = ['id', 'time', 'created_at']
