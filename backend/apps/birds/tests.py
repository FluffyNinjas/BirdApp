from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import BirdSerializer
from .models import Bird, UserBird, Capture
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory


class BirdSerializerTest(TestCase):
    def test_serialize_bird(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        bird = Bird.objects.create(name="Sparrow", icon="sparrow.png", label="sparrow")
        serializer = BirdSerializer(bird, context={'request': request})
        self.assertIn('name', serializer.data)
        self.assertEqual(serializer.data['name'], "Sparrow")

class BirdListAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Bird.objects.create(name="Eagle", icon="eagle.png", label="eagle")
        Bird.objects.create(name="Owl", icon="owl.png", label="owl")

    def test_get_all_birds(self):
        response = self.client.get(reverse('bird-list'))  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class CaptureAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.client.force_authenticate(user=self.user)
        self.bird = Bird.objects.create(name="Parrot", icon="parrot.png", label="parrot")

    def test_capture_creates_record(self):
        data = {"bird_id": self.bird.id, "image": "fake_image.png"}
        response = self.client.post(reverse('capture-bird'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Capture.objects.count(), 1)

class AuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('capture-bird')

    def test_unauthorized_capture(self):
        response = self.client.post(self.url, {"bird_id": 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserProgressTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='birdlover', password='123')
        self.client.force_authenticate(user=self.user)
        self.bird = Bird.objects.create(name="Swan", icon="swan.png", label="swan")
