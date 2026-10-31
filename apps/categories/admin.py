from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'slug', 'icon_name', 'color', 'order', 'is_active', 'article_count']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en', 'slug']
    prepopulated_fields = {'slug': ('name_en',)}
