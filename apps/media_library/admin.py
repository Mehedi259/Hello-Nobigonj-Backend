from django.contrib import admin
from .models import MediaFile

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'file_type', 'size', 'dimensions', 'uploaded_by', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['name']
