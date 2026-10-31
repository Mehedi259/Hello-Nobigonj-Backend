from django.urls import path
from .views import DashboardStatsView, ExportArticlesReportView

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('reports/articles/csv/', ExportArticlesReportView.as_view(), name='export_articles_csv'),
]
