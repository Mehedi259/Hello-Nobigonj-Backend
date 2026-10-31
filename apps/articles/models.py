from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from apps.categories.models import Category
from apps.authors.models import Author

class Article(models.Model):
    STATUS_CHOICES = (
        ('Published', 'প্রকাশিত (Published)'),
        ('Draft', 'খসড়া (Draft)'),
        ('Archived', 'সংরক্ষণাগার (Archived)'),
    )

    title = models.CharField(max_length=300, verbose_name='শিরোনাম')
    slug = models.SlugField(max_length=350, unique=True, blank=True, allow_unicode=True, verbose_name='স্লাগ')
    subtitle = models.CharField(max_length=350, blank=True, null=True, verbose_name='উপ-শিরোনাম')
    excerpt = models.TextField(verbose_name='সংক্ষিপ্ত অংশ')
    content = models.TextField(verbose_name='মূল সংবাদ')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', verbose_name='বিভাগ')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', verbose_name='লেখক')

    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name='সংবাদ ছবি')
    image_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='ছবির লিংক (URL)')
    image_caption = models.CharField(max_length=300, blank=True, null=True, verbose_name='ছবির ক্যাপশন')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Published', verbose_name='অবস্থা')

    # Placement Toggles
    is_hero = models.BooleanField(default=False, verbose_name='প্রধান ব্যানার (Hero)')
    is_breaking = models.BooleanField(default=False, verbose_name='ব্রেকিং নিউজ')
    is_featured = models.BooleanField(default=False, verbose_name='বিশেষ সংবাদ (Featured)')
    is_popular = models.BooleanField(default=False, verbose_name='জনপ্রিয় সংবাদ')

    featured_order = models.PositiveIntegerField(default=0, verbose_name='ফিচার্ড ক্রম')
    popular_rank = models.PositiveIntegerField(default=0, verbose_name='জনপ্রিয় ক্রম')

    views = models.PositiveIntegerField(default=0, verbose_name='পাঠক সংখ্যা (Views)')
    tags = models.JSONField(default=list, blank=True, verbose_name='ট্যাগসমূহ')

    published_at = models.DateTimeField(default=timezone.now, verbose_name='প্রকাশের সময়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'সংবাদ'
        verbose_name_plural = 'সংবাদসমূহ'
        ordering = ['-published_at', '-id']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['is_hero']),
            models.Index(fields=['is_breaking']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_popular']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from title or timestamp
            base_slug = slugify(self.title, allow_unicode=True)
            if not base_slug:
                base_slug = f'article-{int(timezone.now().timestamp())}'
            unique_slug = base_slug
            num = 1
            while Article.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return '/images/padma-bridge.jpg'

    @property
    def time_ago(self):
        now = timezone.now()
        diff = now - self.published_at
        seconds = diff.total_seconds()
        if seconds < 60:
            return 'এইমাত্র'
        minutes = int(seconds // 60)
        if minutes < 60:
            return f'{minutes} মিনিট আগে'
        hours = int(minutes // 60)
        if hours < 24:
            return f'{hours} ঘণ্টা আগে'
        days = int(hours // 24)
        if days < 30:
            return f'{days} দিন আগে'
        return self.published_at.strftime('%d %B %Y')

    @property
    def read_time(self):
        words = len(self.content.split())
        minutes = max(1, round(words / 130))
        return f'{minutes} মিনিট'
