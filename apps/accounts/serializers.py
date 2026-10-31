from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils import timesince
from .models import ActivityLog

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': str(self.user.id),
            'name': self.user.get_full_name() or self.user.username,
            'email': self.user.email,
            'role': self.user.get_role_display(),
            'role_key': self.user.role,
            'avatar': self.user.display_avatar,
            'is_staff': self.user.is_staff,
            'is_superuser': self.user.is_superuser,
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField(read_only=True)
    avatar_display = serializers.CharField(source='display_avatar', read_only=True)
    joined_date = serializers.DateTimeField(source='date_joined', format='%Y-%m-%d', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'status', 'phone', 'avatar', 'avatar_url',
            'avatar_display', 'bio', 'designation', 'location',
            'articles_count', 'joined_date', 'last_login', 'is_active'
        ]
        read_only_fields = ['id', 'joined_date', 'last_login']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'role', 'phone']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ActivityLogSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = ActivityLog
        fields = ['id', 'activity_type', 'title', 'detail', 'time_ago', 'created_at', 'user_name']

    def get_time_ago(self, obj):
        return f'{timesince.timesince(obj.created_at)} আগে'
