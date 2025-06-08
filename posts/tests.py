from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.routers import SimpleRouter
from rest_framework.test import APIClient

from .models import Post
from .views import PostViewSet


class PostAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.router = SimpleRouter()
        self.router.register(r"posts", PostViewSet, basename="post")
        self.url = reverse("post-list")

    def test_create_post(self):
        data = {"title": "Test Post", "content": "This is a test post content."}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, "Test Post")

    def test_list_posts(self):
        Post.objects.create(title="Post 1", content="Content 1")
        Post.objects.create(title="Post 2", content="Content 2")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_post(self):
        post = Post.objects.create(title="Old Title", content="Old Content")
        url = reverse("post-detail", kwargs={"pk": post.pk})
        data = {"title": "Updated Title", "content": "Updated Content"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated Title")

    def test_delete_post(self):
        post = Post.objects.create(title="To be deleted", content="Delete me")
        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_invalid_create_post(self):
        data = {
            "title": "",  # Invalid title
            "content": "This post has an invalid title.",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

    def test_update_nonexistent_post(self):
        url = reverse("post-detail", kwargs={"pk": 999})
        data = {"title": "Nonexistent Post", "content": "This post does not exist."}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_post(self):
        url = reverse("post-detail", kwargs={"pk": 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_empty_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
