from django.db import models
from django.conf import settings
from PIL import Image

class MediaFile(models.Model):
    TYPE_CHOICES = (
        ('image', 'ছবি (Image)'),
        ('document', 'নথি (Document)'),
        ('video', 'ভিডিও (Video)'),
    )

    name = models.CharField(max_length=255, verbose_name='ফাইলের নাম')
    file = models.FileField(upload_to='library/%Y/%m/', verbose_name='ফাইল')
    file_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='বিকল্প ইউআরএল')
    file_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='image', verbose_name='ফাইলের ধরন')
    size = models.CharField(max_length=50, blank=True, verbose_name='সাইজ')
    dimensions = models.CharField(max_length=50, blank=True, null=True, verbose_name='ডাইমেনশন')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'মিডিয়া ফাইল'
        verbose_name_plural = 'মিডিয়া লাইব্রেরি'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file and not self.size:
            size_bytes = self.file.size
            if size_bytes < 1024:
                self.size = f'{size_bytes} B'
            elif size_bytes < 1024 * 1024:
                self.size = f'{round(size_bytes / 1024, 1)} KB'
            else:
                self.size = f'{round(size_bytes / (1024 * 1024), 2)} MB'

        if not self.name and self.file:
            self.name = self.file.name

        super().save(*args, **kwargs)

        # Detect dimensions if image
        if self.file_type == 'image' and self.file and not self.dimensions:
            try:
                with Image.open(self.file.path) as img:
                    w, h = img.size
                    self.dimensions = f'{w}x{h}'
                    MediaFile.objects.filter(id=self.id).update(dimensions=self.dimensions)
            except Exception:
                pass

    @property
    def display_url(self):
        if self.file:
            return self.file.url
        return self.file_url or ''
