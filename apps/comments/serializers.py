from rest_framework import serializers
from .models import Comment
from django.utils import timesince

class CommentSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    article_title = serializers.CharField(source='article.title', read_only=True)
    article_slug = serializers.CharField(source='article.slug', read_only=True)
    articleId = serializers.CharField(source='article.slug', read_only=True)
    authorName = serializers.CharField(source='author_name', read_only=True)
    createdAt = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'articleId', 'article_title', 'article_slug',
            'author_name', 'authorName', 'author_email', 'avatar_url',
            'content', 'likes', 'status', 'parent', 'time_ago',
            'createdAt', 'created_at'
        ]
        read_only_fields = ['id', 'likes', 'created_at']

    def get_time_ago(self, obj):
        return f'{timesince.timesince(obj.created_at)} আগে'

    def get_createdAt(self, obj):
        return obj.created_at.strftime('%d %B %Y, %I:%M %p')

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['article', 'author_name', 'author_email', 'content', 'parent']
