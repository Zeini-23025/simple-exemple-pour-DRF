from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Anime


class AnimeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('anime-list')

    def test_create_anime(self):
        data = {
            "title": "Test Anime",
            "description": "This is a test anime description.",
            "status": "ongoing",
            "classification": "tv"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Anime.objects.count(), 1)
        self.assertEqual(Anime.objects.get().title, "Test Anime")

    def test_list_anime(self):
        Anime.objects.create(title="Anime 1", description="Description 1")
        Anime.objects.create(title="Anime 2", description="Description 2")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_anime(self):
        anime = Anime.objects.create(
            title="Old Title",
            description="Old Description"
        )
        url = reverse('anime-detail', kwargs={'pk': anime.pk})
        data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "status": "completed",
            "classification": "movie"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        anime.refresh_from_db()
        self.assertEqual(anime.title, "Updated Title")
        self.assertEqual(anime.status, "completed")

    def test_delete_anime(self):
        anime = Anime.objects.create(
            title="To be deleted", description="Delete me"
        )
        url = reverse('anime-detail', kwargs={'pk': anime.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Anime.objects.count(), 0)

    def test_invalid_create_anime(self):
        data = {
            "title": "",  # titre invalide (champ requis)
            "description": "This anime has an invalid title.",
            "status": "ongoing",
            "classification": "tv"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Anime.objects.count(), 0)
