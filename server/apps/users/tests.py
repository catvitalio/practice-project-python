from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()

        self.user_create_instance = {'username': 'instance', 'password': 'test'}
        self.user_auth_instance = {'username': 'test', 'password': 'test'}

    def test_create_user(self):
        """
        Test POST return 'id', 'username', 'token' fields
        """
        url = reverse('users-list')
        response = self.client.post(url, self.user_create_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue('id' in response.data)
        self.assertTrue('username' in response.data)
        self.assertTrue('token' in response.data)
        self.assertFalse('password' in response.data)

    def test_auth_user(self):
        """
        Test POST return 'token' field
        """
        url = reverse('auth-list')
        response = self.client.post(url, self.user_auth_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
