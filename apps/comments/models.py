from django.db import models
from django.conf import settings
from apps.articles.models import Article

class Comment(models.Model):
    STATUS_CHOICES = (
        ('Approved', 'অনুমোদিত (Approved)'),
        ('Pending', 'বিচারাধীন (Pending)'),
        ('Spam', 'স্প্যাম (Spam)'),
    )

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='সংবাদ')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    author_name = models.CharField(max_length=150, default='পাঠক', verbose_name='মন্তব্যকারীর নাম')
    author_email = models.EmailField(blank=True, null=True, verbose_name='ইমেইল')
    avatar_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='অবতার ইউআরএল')
    content = models.TextField(verbose_name='মন্তব্য')
    likes = models.PositiveIntegerField(default=0, verbose_name='লাইক সংখ্যা')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Approved', verbose_name='অবস্থা')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'মন্তব্য'
        verbose_name_plural = 'মন্তব্যসমূহ'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} on {self.article.title[:30]}'
