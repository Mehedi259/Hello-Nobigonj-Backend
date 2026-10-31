from django.db import models
from django.utils import timesince

class Notification(models.Model):
    TYPE_CHOICES = (
        ('info', 'তথ্য (Info)'),
        ('success', 'সফলতা (Success)'),
        ('warning', 'সতর্কতা (Warning)'),
    )

    title = models.CharField(max_length=200, verbose_name='শিরোনাম')
    description = models.TextField(verbose_name='বিবরণ')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info', verbose_name='ধরন')
    read = models.BooleanField(default=False, verbose_name='পঠিত')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'নোটিফিকেশন'
        verbose_name_plural = 'নোটিফিকেশনসমূহ'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} (Read: {self.read})'

    @property
    def time_ago(self):
        return f'{timesince.timesince(self.created_at)} আগে'
