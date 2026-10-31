from rest_framework import serializers
from .models import Subscriber

class SubscriberSerializer(serializers.ModelSerializer):
    subscribedDate = serializers.DateTimeField(source='subscribed_date', format='%b %d, %Y', read_only=True)

    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'status', 'subscribedDate', 'subscribed_date']
        read_only_fields = ['id', 'subscribedDate', 'subscribed_date']
