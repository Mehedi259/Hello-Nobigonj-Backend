from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from apps.accounts.permissions import IsEditorOrSuperAdmin

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [IsEditorOrSuperAdmin]

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.read = True
        notif.save(update_fields=['read'])
        return Response({'success': True, 'read': True})

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        Notification.objects.filter(read=False).update(read=True)
        return Response({'success': True, 'message': 'All marked as read'})

    @action(detail=False, methods=['post'], url_path='clear-all')
    def clear_all(self, request):
        Notification.objects.all().delete()
        return Response({'success': True, 'message': 'All notifications cleared'})
