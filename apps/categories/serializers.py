from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(read_only=True)
    count = serializers.IntegerField(source='article_count', read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'name_en', 'slug', 'icon_name',
            'color', 'description', 'order', 'is_active',
            'article_count', 'count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
