from rest_framework import serializers
from .models import MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='display_url', read_only=True)
    uploadedDate = serializers.DateTimeField(source='created_at', format='%b %d, %Y', read_only=True)
    type = serializers.CharField(source='file_type')

    class Meta:
        model = MediaFile
        fields = [
            'id', 'name', 'file', 'file_url', 'url', 'size',
            'type', 'file_type', 'dimensions', 'uploaded_by',
            'uploadedDate', 'created_at'
        ]
        read_only_fields = ['id', 'size', 'dimensions', 'uploadedDate', 'created_at']
