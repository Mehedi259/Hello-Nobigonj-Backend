from django.urls import path
from .views import SiteSettingView, ContactMessageCreateView, ContactMessageListView

urlpatterns = [
    path('', SiteSettingView.as_view(), name='site_settings'),
    path('contact/', ContactMessageCreateView.as_view(), name='contact_create'),
    path('contact/messages/', ContactMessageListView.as_view(), name='contact_list'),
]
