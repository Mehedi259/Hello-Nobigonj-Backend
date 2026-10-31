from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email', 'location', 'articles_count', 'is_active', 'joined_date']
    list_filter = ['is_active', 'role', 'location']
    search_fields = ['name', 'email', 'bio']
