from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from apps.accounts.permissions import IsEditorOrSuperAdmin

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('article').all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'article', 'article__slug']
    search_fields = ['author_name', 'author_email', 'content', 'article__title']
    ordering_fields = ['created_at', 'likes']

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'retrieve', 'like']:
            return [permissions.AllowAny()]
        return [IsEditorOrSuperAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        # Non-staff users only see Approved comments
        if not (self.request.user and self.request.user.is_authenticated and self.request.user.is_staff):
            if self.action in ['list', 'retrieve']:
                qs = qs.filter(status='Approved')
        return qs

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        comment = self.get_object()
        Comment.objects.filter(id=comment.id).update(likes=F('likes') + 1)
        comment.refresh_from_db()
        return Response({'success': True, 'likes': comment.likes})

    @action(detail=True, methods=['post'], permission_classes=[IsEditorOrSuperAdmin])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment.status = 'Approved'
        comment.save(update_fields=['status'])
        return Response({'success': True, 'status': comment.status})

    @action(detail=True, methods=['post'], permission_classes=[IsEditorOrSuperAdmin])
    def mark_spam(self, request, pk=None):
        comment = self.get_object()
        comment.status = 'Spam'
        comment.save(update_fields=['status'])
        return Response({'success': True, 'status': comment.status})
