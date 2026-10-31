from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'is_hero', 'is_breaking', 'is_featured', 'views', 'published_at']
    list_filter = ['status', 'category', 'is_hero', 'is_breaking', 'is_featured', 'published_at']
    search_fields = ['title', 'subtitle', 'excerpt', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
