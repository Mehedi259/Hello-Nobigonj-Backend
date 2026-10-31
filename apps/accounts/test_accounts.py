from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.subscribers.models import Subscriber
from apps.categories.models import Category
from apps.authors.models import Author
from apps.articles.models import Article

User = get_user_model()

class CoreAuthAndWorkflowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@hellodesh.com',
            username='admin',
            password='adminpassword123',
            role='superadmin'
        )

    def test_admin_jwt_login(self):
        url = '/api/v1/auth/login/'
        response = self.client.post(url, {
            'email': 'admin@hellodesh.com',
            'password': 'adminpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], 'admin@hellodesh.com')

    def test_subscriber_creation(self):
        url = '/api/v1/subscribers/'
        response = self.client.post(url, {'email': 'newuser@example.com'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscriber.objects.filter(email='newuser@example.com').exists())

    def test_dashboard_stats_authenticated(self):
        # Login admin client
        login_resp = self.client.post('/api/v1/auth/login/', {
            'email': 'admin@hellodesh.com',
            'password': 'adminpassword123'
        })
        token = login_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = '/api/v1/analytics/dashboard/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('kpis', response.data)
        self.assertIn('views_trend', response.data)
