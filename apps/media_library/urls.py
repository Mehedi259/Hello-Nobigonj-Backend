from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaFileViewSet

router = DefaultRouter()
router.register(r'', MediaFileViewSet, basename='media')

urlpatterns = [
    path('', include(router.urls)),
]
