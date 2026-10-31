from django.db import models

class Subscriber(models.Model):
    STATUS_CHOICES = (
        ('Active', 'সক্রিয় (Active)'),
        ('Unsubscribed', 'বাতিল (Unsubscribed)'),
    )

    email = models.EmailField(unique=True, verbose_name='ইমেইল ঠিকানা')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', verbose_name='অবস্থা')
    subscribed_date = models.DateTimeField(auto_now_add=True, verbose_name='নিবন্ধনের তারিখ')

    class Meta:
        verbose_name = 'নিউজলেটার গ্রাহক'
        verbose_name_plural = 'নিউজলেটার গ্রাহকবৃন্দ'
        ordering = ['-subscribed_date']

    def __str__(self):
        return f'{self.email} ({self.status})'
