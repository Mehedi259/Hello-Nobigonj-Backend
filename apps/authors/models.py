from django.db import models
from django.conf import settings

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='author_profile')
    name = models.CharField(max_length=150, verbose_name='লেখকের নাম')
    role = models.CharField(max_length=100, default='প্রতিবেদক', verbose_name='পদবি / ভূমিকা')
    email = models.EmailField(unique=True, verbose_name='ইমেইল')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='ফোন নম্বর')
    avatar = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name='ছবি')
    avatar_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='ছবির ইউআরএল')
    bio = models.TextField(blank=True, null=True, verbose_name='সংক্ষিপ্ত পরিচিতি')
    location = models.CharField(max_length=100, default='ঢাকা', verbose_name='কর্মস্থল / অবস্থান')
    joined_date = models.DateField(auto_now_add=True, verbose_name='যোগদানের তারিখ')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'প্রতিবেদক / লেখক'
        verbose_name_plural = 'প্রতিবেদক ও লেখকবৃন্দ'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.role}'

    @property
    def display_avatar(self):
        if self.avatar:
            return self.avatar.url
        if self.avatar_url:
            return self.avatar_url
        return '/images/reporter-rakib.jpg'

    @property
    def articles_count(self):
        return getattr(self, 'articles', None).filter(status='Published').count() if hasattr(self, 'articles') else 0
