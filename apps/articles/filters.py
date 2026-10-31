import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    category_id = django_filters.NumberFilter(field_name='category__id')
    status = django_filters.CharFilter(field_name='status')
    is_hero = django_filters.BooleanFilter(field_name='is_hero')
    is_breaking = django_filters.BooleanFilter(field_name='is_breaking')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')
    is_popular = django_filters.BooleanFilter(field_name='is_popular')
    author_id = django_filters.NumberFilter(field_name='author__id')
    published_after = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')

    class Meta:
        model = Article
        fields = [
            'category', 'category_id', 'status', 'is_hero',
            'is_breaking', 'is_featured', 'is_popular', 'author_id'
        ]
