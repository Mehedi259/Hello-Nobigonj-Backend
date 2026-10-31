from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='বাংলা নাম')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='ইংরেজি নাম')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='স্লাগ')
    icon_name = models.CharField(max_length=50, default='Layers', verbose_name='আইকন কোড')
    color = models.CharField(max_length=20, default='#dc2626', verbose_name='রং কোড (HEX)')
    description = models.TextField(blank=True, null=True, verbose_name='বিবরণ')
    order = models.PositiveIntegerField(default=0, verbose_name='ক্রম')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='তৈরির তারিখ')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='হালনাগাদ তারিখ')

    class Meta:
        verbose_name = 'বিভাগ'
        verbose_name_plural = 'বিভাগসমূহ'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.name} ({self.name_en or self.slug})'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def article_count(self):
        return getattr(self, 'articles', None).filter(status='Published').count() if hasattr(self, 'articles') else 0
