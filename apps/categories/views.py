from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategorySerializer
from apps.accounts.permissions import IsEditorOrSuperAdmin

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('order', 'id')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'name_en', 'slug', 'description']
    ordering_fields = ['order', 'name', 'created_at']
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsEditorOrSuperAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        # Non-staff readers only see active categories
        if not (self.request.user and self.request.user.is_authenticated and self.request.user.is_staff):
            if self.action == 'list':
                qs = qs.filter(is_active=True)
        return qs
