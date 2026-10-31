from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'article', 'status', 'likes', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['author_name', 'author_email', 'content', 'article__title']
