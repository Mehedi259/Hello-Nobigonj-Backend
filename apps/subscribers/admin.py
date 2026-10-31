from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'status', 'subscribed_date']
    list_filter = ['status', 'subscribed_date']
    search_fields = ['email']
