from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import MediaFile
from .serializers import MediaFileSerializer
from apps.accounts.permissions import IsReporterOrAbove

class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all().order_by('-created_at')
    serializer_class = MediaFileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsReporterOrAbove]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_type']
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(uploaded_by=user)
