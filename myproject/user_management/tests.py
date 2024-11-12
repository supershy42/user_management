from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserRegistrationTest(APITestCase):

    def setUp(self):
        # 초기 사용자 생성으로 중복 테스트 준비
        self.existing_user_data = {
            'nickname': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Testpass123!'
        }
        User.objects.create_user(**self.existing_user_data)

    def test_user_registration_success(self):
        # 정상적인 회원가입 테스트
        data = {
            'nickname': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Newpass123!'
        }

        url = reverse('register')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Registration successful", response.data.get("message", ""))

        user_exists = User.objects.filter(email=data['email']).exists()
        self.assertTrue(user_exists)

    def test_user_registration_duplicate_email(self):
        # 중복 이메일로 회원가입 시도
        data = {
            'nickname': 'uniqueuser',
            'email': self.existing_user_data['email'],  # 중복 이메일
            'password': 'Testpass123!'
        }

        url = reverse('register')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("already exists", response.data["email"][0])

    def test_user_registration_duplicate_nickname(self):
        # 중복 닉네임으로 회원가입 시도
        data = {
            'nickname': self.existing_user_data['nickname'],  # 중복 닉네임
            'email': 'uniqueuser@example.com',
            'password': 'Testpass123!'
        }

        url = reverse('register')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nickname", response.data)
        self.assertIn("This nickname is already taken.", response.data["nickname"][0])  # 예상 메시지로 수정

