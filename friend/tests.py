from rest_framework.test import APITestCase
from django.urls import reverse
from .models import FriendRequest, Friendship
from django.contrib.auth import get_user_model

User = get_user_model()

class FriendRequestTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@example.com", password="password1", nickname="user1")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password1", nickname="user2")
        self.client.force_authenticate(user=self.user1)

    def test_send_friend_request_success(self):
        # 친구 요청 성공
        url = reverse('request')
        data = {'to_user_id': self.user2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FriendRequest.objects.count(), 1)

    def test_send_friend_request_duplicate(self):
        # 중복된 친구 요청
        FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        url = reverse('request')
        data = {'to_user_id': self.user2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)


class RespondToFriendRequestTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@example.com", password="password1", nickname="user1")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password1", nickname="user2")
        self.client.force_authenticate(user=self.user1)

    def test_accept_friend_request_success(self):
        # 친구 요청 수락
        friend_request = FriendRequest.objects.create(from_user=self.user2, to_user=self.user1)
        url = reverse('respond')
        data = {'friend_request_id': friend_request.id, 'action': 'accept'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friendship.objects.count(), 1)
        self.assertEqual(Friendship.objects.first().user1, self.user2)
        self.assertEqual(Friendship.objects.first().user2, self.user1)


class FriendListTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@example.com", password="password1", nickname="user1")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password1", nickname="user2")
        self.client.force_authenticate(user=self.user1)

    def test_friend_list_with_friends(self):
        # 친구 목록 조회
        Friendship.objects.create(user1=self.user1, user2=self.user2)
        url = reverse('list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.user2.id)

    def test_friend_list_no_friends(self):
        # 친구가 없는 경우
        url = reverse('list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], "No friends found.")