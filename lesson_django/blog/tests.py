from django.test import TestCase
from django.urls import reverse
from .models import Blog


class BlogListDetailTests(TestCase):

    def setUp(self):
        self.blog = Blog.objects.create(title="Тестовая статья", content="Текст статьи")

    def test_list_returns_200(self):
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_contains_blog_title(self):
        response = self.client.get(reverse("blog_list"))
        self.assertContains(response, "Тестовая статья")

    def test_detail_returns_200(self):
        response = self.client.get(reverse("blog_detail", args=[self.blog.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_contains_content(self):
        response = self.client.get(reverse("blog_detail", args=[self.blog.pk]))
        self.assertContains(response, "Текст статьи")

    def test_detail_nonexistent_id_returns_404(self):
        response = self.client.get(reverse("blog_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_list_link_leads_to_detail(self):
        detail_url = reverse("blog_detail", args=[self.blog.pk])
        list_response = self.client.get(reverse("blog_list"))
        self.assertContains(list_response, detail_url)
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, 200)


class BlogLikesTests(TestCase):

    def setUp(self):
        self.blog = Blog.objects.create(title="Статья", content="Текст")

    def test_new_blog_has_zero_likes(self):
        self.assertEqual(self.blog.likes, 0)

    def test_detail_view_increments_likes(self):
        self.client.get(reverse("blog_detail", args=[self.blog.pk]))
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.likes, 1)