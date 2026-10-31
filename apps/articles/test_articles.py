from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.categories.models import Category
from apps.authors.models import Author
from apps.articles.models import Article

class ArticleAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='জাতীয়', slug='national', color='#2563eb')
        self.author = Author.objects.create(name='ডেস্ক রিপোর্ট', email='desk@hellodesh.com')
        self.article = Article.objects.create(
            title='টেস্ট শিরোনাম',
            slug='test-title',
            excerpt='টেস্ট সংক্ষিপ্ত অংশ',
            content='টেস্ট মূল সংবাদ প্রতিবেদন',
            category=self.category,
            author=self.author,
            status='Published',
            is_hero=True,
            views=10
        )

    def test_list_articles(self):
        url = '/api/v1/articles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_retrieve_article_by_slug(self):
        url = f'/api/v1/articles/{self.article.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'টেস্ট শিরোনাম')

    def test_hero_endpoint(self):
        url = '/api/v1/articles/hero/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], 'test-title')

    def test_increment_view(self):
        url = f'/api/v1/articles/{self.article.slug}/view/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.views, 11)
