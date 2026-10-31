from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superadmin')
        extra_fields.setdefault('status', 'active')
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('editor', 'Editor'),
        ('reporter', 'Reporter'),
        ('user', 'Reader'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('banned', 'Banned'),
    )

    email = models.EmailField(unique=True, verbose_name='ইমেইল')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name='ভূমিকা')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='অবস্থা')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='ফোন')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='প্রোফাইল ছবি')
    avatar_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='ছবির ইউআরএল')
    bio = models.TextField(blank=True, null=True, verbose_name='জীবনবৃত্তান্ত')
    designation = models.CharField(max_length=100, blank=True, null=True, verbose_name='পদবি')
    location = models.CharField(max_length=100, blank=True, null=True, default='ঢাকা', verbose_name='অবস্থান')

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'ব্যবহারকারী'
        verbose_name_plural = 'ব্যবহারকারীগণ'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def articles_count(self):
        return getattr(self, 'articles', None).count() if hasattr(self, 'articles') else 0

    @property
    def display_avatar(self):
        if self.avatar:
            return self.avatar.url
        if self.avatar_url:
            return self.avatar_url
        return '/images/admin-avatar.jpg'

class ActivityLog(models.Model):
    TYPE_CHOICES = (
        ('publish', 'সংবাদ প্রকাশ'),
        ('register', 'নতুন নিবন্ধন'),
        ('comment', 'মন্তব্য'),
        ('subscribe', 'সাবস্ক্রিপশন'),
        ('update', 'হালনাগাদ'),
        ('delete', 'মুছে ফেলা'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='কার্যক্রম ধরন')
    title = models.CharField(max_length=255, verbose_name='শিরোনাম')
    detail = models.TextField(blank=True, null=True, verbose_name='বিবরণ')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='আইপি অ্যাড্রেস')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='সময়')

    class Meta:
        verbose_name = 'কার্যক্রম লগ'
        verbose_name_plural = 'কার্যক্রম লগসমূহ'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'
