from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from .models import Article
from .filters import ArticleFilter
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleWriteSerializer
)
from apps.accounts.permissions import IsEditorOrSuperAdmin, IsReporterOrAbove

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('category', 'author').all().order_by('-published_at', '-id')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ['title', 'subtitle', 'excerpt', 'content', 'tags', 'category__name', 'author__name']
    ordering_fields = ['published_at', 'views', 'id', 'featured_order', 'popular_rank']
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'hero', 'breaking', 'featured', 'popular', 'latest', 'increment_view']:
            return [permissions.AllowAny()]
        return [IsReporterOrAbove()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleWriteSerializer
        return ArticleListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # For public readers, only serve Published articles
        if not (self.request.user and self.request.user.is_authenticated and self.request.user.is_staff):
            if self.action not in ['update', 'partial_update', 'destroy']:
                qs = qs.filter(status='Published')
        return qs

    @action(detail=True, methods=['post'], url_path='view')
    def increment_view(self, request, slug=None):
        article = self.get_object()
        Article.objects.filter(id=article.id).update(views=F('views') + 1)
        article.refresh_from_db()
        return Response({'success': True, 'views': article.views})

    @action(detail=False, methods=['get'])
    def hero(self, request):
        hero_article = self.get_queryset().filter(is_hero=True).first()
        if not hero_article:
            hero_article = self.get_queryset().first()
        if hero_article:
            serializer = ArticleDetailSerializer(hero_article, context={'request': request})
            return Response(serializer.data)
        return Response({'message': 'No hero article available'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def breaking(self, request):
        breaking_news = self.get_queryset().filter(is_breaking=True)[:8]
        serializer = ArticleListSerializer(breaking_news, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_news = self.get_queryset().filter(is_featured=True).order_by('featured_order', '-published_at')[:6]
        serializer = ArticleListSerializer(featured_news, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_news = self.get_queryset().order_by('-views', 'popular_rank')[:6]
        serializer = ArticleListSerializer(popular_news, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_news = self.get_queryset().order_by('-published_at')[:10]
        serializer = ArticleListSerializer(latest_news, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsEditorOrSuperAdmin])
    def bulk_action(self, request):
        action_type = request.data.get('action')
        article_ids = request.data.get('ids', [])

        if not action_type or not article_ids:
            return Response({'error': 'action and ids list are required'}, status=status.HTTP_400_BAD_REQUEST)

        articles = Article.objects.filter(id__in=article_ids)
        if action_type == 'publish':
            articles.update(status='Published')
        elif action_type == 'draft':
            articles.update(status='Draft')
        elif action_type == 'archive':
            articles.update(status='Archived')
        elif action_type == 'delete':
            articles.delete()
        else:
            return Response({'error': f'Unsupported action {action_type}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': True, 'affected_count': len(article_ids)})
