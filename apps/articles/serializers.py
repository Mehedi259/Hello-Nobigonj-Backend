from rest_framework import serializers
from .models import Article
from apps.categories.serializers import CategorySerializer
from apps.authors.serializers import AuthorSerializer
from apps.categories.models import Category
from apps.authors.models import Author

class ArticleAuthorSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='display_avatar', read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'role', 'location', 'avatar']

class ArticleListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    categorySlug = serializers.CharField(source='category.slug', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    image = serializers.CharField(source='display_image', read_only=True)
    author = ArticleAuthorSerializer(read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    timeAgo = serializers.CharField(source='time_ago', read_only=True)
    publishedAt = serializers.DateTimeField(source='published_at', format='%d %B %Y, %I:%M %p', read_only=True)
    publishedDate = serializers.DateTimeField(source='published_at', format='%b %d, %Y', read_only=True)
    readTime = serializers.CharField(source='read_time', read_only=True)
    isHero = serializers.BooleanField(source='is_hero', read_only=True)
    isBreaking = serializers.BooleanField(source='is_breaking', read_only=True)
    isFeatured = serializers.BooleanField(source='is_featured', read_only=True)
    isPopular = serializers.BooleanField(source='is_popular', read_only=True)
    featuredOrder = serializers.IntegerField(source='featured_order', read_only=True)
    popularRank = serializers.IntegerField(source='popular_rank', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'subtitle', 'excerpt',
            'category', 'categorySlug', 'category_id', 'category_color',
            'image', 'image_caption', 'author', 'author_name',
            'status', 'views', 'tags', 'publishedAt', 'publishedDate',
            'timeAgo', 'readTime', 'isHero', 'isBreaking',
            'isFeatured', 'isPopular', 'featuredOrder', 'popularRank'
        ]

class ArticleDetailSerializer(ArticleListSerializer):
    content = serializers.CharField()
    prev_article = serializers.SerializerMethodField()
    next_article = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + ['content', 'prev_article', 'next_article', 'comments_count']

    def get_prev_article(self, obj):
        prev = Article.objects.filter(status='Published', published_at__lt=obj.published_at).order_by('-published_at').first()
        if prev:
            return {'id': prev.id, 'title': prev.title, 'slug': prev.slug}
        return None

    def get_next_article(self, obj):
        nxt = Article.objects.filter(status='Published', published_at__gt=obj.published_at).order_by('published_at').first()
        if nxt:
            return {'id': nxt.id, 'title': nxt.title, 'slug': nxt.slug}
        return None

    def get_comments_count(self, obj):
        return getattr(obj, 'comments', None).filter(status='Approved').count() if hasattr(obj, 'comments') else 0

class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'subtitle', 'excerpt', 'content',
            'category', 'author', 'image', 'image_url', 'image_caption',
            'status', 'is_hero', 'is_breaking', 'is_featured', 'is_popular',
            'featured_order', 'popular_rank', 'views', 'tags', 'published_at'
        ]
        read_only_fields = ['id', 'views']
