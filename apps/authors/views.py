from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author
from .serializers import AuthorSerializer
from apps.accounts.permissions import IsEditorOrSuperAdmin

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'role', 'location']
    search_fields = ['name', 'email', 'role', 'bio', 'location']
    ordering_fields = ['name', 'joined_date', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsEditorOrSuperAdmin()]
