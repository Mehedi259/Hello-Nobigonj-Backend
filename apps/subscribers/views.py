import csv
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Subscriber
from .serializers import SubscriberSerializer
from apps.accounts.permissions import IsEditorOrSuperAdmin

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('-subscribed_date')
    serializer_class = SubscriberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['email']
    ordering_fields = ['subscribed_date', 'email']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsEditorOrSuperAdmin()]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip().lower()
        if not email or '@' not in email:
            return Response({'error': 'সঠিক ইমেইল ঠিকানা দিন'}, status=status.HTTP_400_BAD_REQUEST)

        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={'status': 'Active'}
        )
        if not created:
            if subscriber.status == 'Unsubscribed':
                subscriber.status = 'Active'
                subscriber.save()
                return Response({'message': 'আপনার সাবস্ক্রিপশন পুনরায় সচল করা হয়েছে!'}, status=status.HTTP_200_OK)
            return Response({'message': 'আপনি ইতোমধ্যে সাবস্ক্রাইব করেছেন!'}, status=status.HTTP_200_OK)

        return Response({'message': 'ধন্যবাদ! সফলভাবে সাবস্ক্রাইব করা হয়েছে।'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsEditorOrSuperAdmin])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="hellodesh_subscribers.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Email', 'Status', 'Subscribed Date'])
        for s in Subscriber.objects.all():
            writer.writerow([s.id, s.email, s.status, s.subscribed_date.strftime('%Y-%m-%d %H:%M')])
        return response
