from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField(read_only=True)
    display_avatar = serializers.CharField(read_only=True)

    class Meta:
        model = Author
        fields = [
            'id', 'name', 'role', 'email', 'phone',
            'avatar', 'avatar_url', 'display_avatar', 'bio',
            'location', 'joined_date', 'articles_count', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'joined_date', 'created_at', 'updated_at']
