from django.db import models

class SiteSetting(models.Model):
    site_title = models.CharField(max_length=200, default='হ্যালো দেশ | আমার বাংলা', verbose_name='ওয়েবসাইটের নাম')
    tagline = models.CharField(max_length=300, default='সত্য খবর, সবার আগে', verbose_name='ট্যাগলাইন')
    logo = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name='লোগো')
    logo_url = models.CharField(max_length=500, default='/logo.png', verbose_name='লোগো লিংক')
    favicon_url = models.CharField(max_length=500, default='/favicon.ico', verbose_name='ফেভিকন লিংক')

    contact_email = models.EmailField(default='contact@hellodesh.com', verbose_name='যোগাযোগের ইমেইল')
    contact_phone = models.CharField(max_length=50, default='+৮৮০ ১৭০০-০০০০০০', verbose_name='ফোন নম্বর')
    office_address = models.TextField(default='কারওয়ান বাজার, ঢাকা-১২১৫, বাংলাদেশ', verbose_name='ঠিকানা')

    facebook_url = models.URLField(blank=True, default='https://facebook.com')
    twitter_url = models.URLField(blank=True, default='https://x.com')
    youtube_url = models.URLField(blank=True, default='https://youtube.com')
    instagram_url = models.URLField(blank=True, default='https://instagram.com')

    meta_title = models.CharField(max_length=255, default='হ্যালো দেশ - সত্য খবর, সবার আগে', verbose_name='এসইও মেটা টাইটেল')
    meta_description = models.TextField(default='বাংলাদেশের শীর্ষস্থানীয় ডিজিটাল সংবাদ মাধ্যম। ২৪ ঘণ্টা সর্বশেষ খবর, রাজনীতি, অর্থনীতি ও খেলাধুলা।', verbose_name='মেটা বিবরণ')
    meta_keywords = models.CharField(max_length=500, default='বাংলাদেশ সংবাদ, হ্যালো দেশ, ব্রেকিং নিউজ, রাজনীতি, অর্থনীতি', verbose_name='কি-ওয়ার্ডস')

    footer_copyright = models.CharField(max_length=255, default='© ২০২৬ HelloDesh. All rights reserved. সত্যের পক্ষে, মানুষের পাশে।', verbose_name='কপিরাইট বার্তা')
    enable_comments = models.BooleanField(default=True, verbose_name='মন্তব্য চালু রাখুন')
    enable_newsletter = models.BooleanField(default=True, verbose_name='নিউজলেটার চালু রাখুন')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ওয়েবসাইট সেটিংস'
        verbose_name_plural = 'ওয়েবসাইট সেটিংস'

    def __str__(self):
        return self.site_title

    @classmethod
    def get_settings(cls):
        setting, _ = cls.objects.get_or_create(id=1)
        return setting

class ContactMessage(models.Model):
    name = models.CharField(max_length=150, verbose_name='প্রেরকের নাম')
    email = models.EmailField(verbose_name='ইমেইল')
    subject = models.CharField(max_length=250, blank=True, null=True, verbose_name='বিষয়')
    message = models.TextField(verbose_name='বার্তা')
    is_read = models.BooleanField(default=False, verbose_name='পঠিত')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'যোগাযোগ বার্তা'
        verbose_name_plural = 'যোগাযোগ বার্তাসমূহ'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.email}'
