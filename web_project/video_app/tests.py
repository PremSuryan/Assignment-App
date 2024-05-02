from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Video

class VideoAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_video(self):
        data = {'name': 'Test Video', 'video_url': 'https://example.com/video.mp4'}
        response = self.client.post('/api/videos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(Video.objects.get().name, 'Test Video')

    def test_get_video(self):
        video = Video.objects.create(name='Test Video', video_url='https://example.com/video.mp4', user=self.user)
        response = self.client.get(f'/api/videos/{video.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Video')