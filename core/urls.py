from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # OpenAPI 3 Schema & Interactive Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API v1 Endpoints
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/categories/', include('apps.categories.urls')),
    path('api/v1/authors/', include('apps.authors.urls')),
    path('api/v1/articles/', include('apps.articles.urls')),
    path('api/v1/comments/', include('apps.comments.urls')),
    path('api/v1/media/', include('apps.media_library.urls')),
    path('api/v1/subscribers/', include('apps.subscribers.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/settings/', include('apps.settings_app.urls')),

    # Direct /api/ aliases
    path('api/auth/', include('apps.accounts.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/authors/', include('apps.authors.urls')),
    path('api/articles/', include('apps.articles.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/media/', include('apps.media_library.urls')),
    path('api/subscribers/', include('apps.subscribers.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/settings/', include('apps.settings_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
