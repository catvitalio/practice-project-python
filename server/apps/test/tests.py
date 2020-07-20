from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.test.models import Test


class TestSignalTests(TestCase):
    def test_random_string_is_generated(self):
        """
        Test that `random_string` field was filled by random value
        """
        count_before = Test.objects.count()

        name = 'Just a name'

        test_instance = Test.objects.create(name=name)
        self.assertEqual(Test.objects.count(), count_before + 1)

        self.assertEqual(test_instance.name, name)
        self.assertEqual(type(test_instance.random_string), str)
        self.assertEqual(len(test_instance.random_string), 32)


class NumPairAPITests(APITestCase):
    def setUp(self):
        Test.objects.create(name='first obj')
        Test.objects.create(name='second obj')

        self.count_before = Test.objects.count()

        self.test_instance = {'name': 'Test instance'}
        self.test_incorrect_instance = {'name': 'Wrong', 'random_string': 'instance'}

    def test_create_action_correct_instance(self):
        """
        Test POST works with only `name` field
        """
        url = reverse('test-list')
        response = self.client.post(url, self.test_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.count(), self.count_before + 1)

        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('random_string' in response.data)

        self.assertEqual(self.test_instance['name'], response.data['name'])
        self.assertEqual(type(response.data['random_string']), str)

    def test_create_action_incorrect_instance(self):
        """
        Test POST ignore `random_string` field
        """
        url = reverse('test-list')
        response = self.client.post(url, self.test_incorrect_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.count(), self.count_before + 1)

        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('random_string' in response.data)

        self.assertEqual(self.test_incorrect_instance['name'], response.data['name'])
        self.assertTrue(type(response.data['random_string']), str)
        self.assertTrue(response.data['random_string'] != self.test_incorrect_instance['random_string'])

    def test_list_action(self):
        """
        Test that `list` action for Test returns list of objects with all fields
        """
        url = reverse('test-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.count_before)

    def test_retrieve_action(self):
        """
        Test that GET by id returns correct data.
        """
        obj = Test.objects.first()

        url = reverse('test-detail', args=(obj.id, ))
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], obj.id)
        self.assertEqual(response.data['name'], obj.name)
        self.assertEqual(response.data['random_string'], obj.random_string)

    def test_retrieve_wrong_id_action(self):
        """
        Test that GET by wrong id returns 404.
        """
        obj = Test.objects.order_by('id').last()

        url = reverse('test-detail', args=(obj.id+1, ))
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_action(self):
        """
        Test that PUT, PATCH not allowed.
        """
        obj = Test.objects.first()

        url = reverse('test-detail', args=(obj.id, ))
        response = self.client.put(url, self.test_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_action(self):
        """
        Test that DELETE not allowed.
        """
        obj = Test.objects.first()

        url = reverse('test-detail', args=(obj.id, ))
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
