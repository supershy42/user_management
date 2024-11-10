from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserRegistrationTest(APITestCase):
    def test_user_registration(self):

        data = {
            'nickname': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Testpass123!'
        }

        url = reverse('register')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIn("Registration successful", response.data.get("message", ""))
        
        from .models import User
        user_exists = User.objects.filter(email=data['email']).exists()
        self.assertTrue(user_exists)
