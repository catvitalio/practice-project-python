from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.eats.models import Place, User, Ingredient


class IngredientTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()

        self.token = Token.objects.get(user__username=user)

        self.ingredient_instance = {'name': 'test', 'calories': 5}

    def test_create_ingredient(self):
        """
        Test POST works only with auth token
        """
        url = reverse('ingredients-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, self.ingredient_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ingredient_without_token(self):
        """
        Test POST without token returns 401
        """
        url = reverse('ingredients-list')

        response = self.client.post(url, self.ingredient_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PlaceTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(username='test')
        self.owner.set_password('test')
        self.owner.save()

        self.not_owner = User.objects.create(username='not_owner')
        self.not_owner.set_password('test')
        self.not_owner.save()

        self.token = Token.objects.get(user__username=self.owner)
        self.not_owner_token = Token.objects.get(user__username=self.not_owner)

        Place.objects.create(name='test', address='Moscow', owner=self.owner)
        self.place_instance = {'name': 'instance', 'address': 'Krasnoyarsk'}

    def test_list_place(self):
        """
        Test GET works without authorization
        """
        url = reverse('places-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_place(self):
        """
        Test LIST works without authorization
        """
        obj = Place.objects.first()
        url = reverse('places-detail', args=(obj.id, ))

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_place(self):
        """
        Test POST works only with auth token
        """
        url = reverse('places-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_place_without_token(self):
        """
        Test POST without token returns 401
        """
        url = reverse('places-list')

        response = self.client.post(url, self.place_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_place(self):
        """
        Test PUT, PATCH works only for owners of places
        """
        obj = Place.objects.first()
        url = reverse('places-detail', args=(obj.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(obj.owner == self.owner)

        response = self.client.patch(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(obj.owner == self.owner)

    def test_update_not_owner_place(self):
        """
        Test PUT, PATCH with wrong owner token returns 403
        """
        obj = Place.objects.first()
        url = reverse('places-detail', args=(obj.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.not_owner_token.key)
        response = self.client.put(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(obj.owner == self.not_owner)

        response = self.client.patch(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(obj.owner == self.not_owner)

    def test_delete_place(self):
        """
        Test DELETE works only for owners of places
        """
        obj = Place.objects.first()
        url = reverse('places-detail', args=(obj.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(obj.owner == self.owner)

    def test_delete_not_owner_place(self):
        """
        Test DELETE with wrong owner token returns 403
        """
        obj = Place.objects.first()
        url = reverse('places-detail', args=(obj.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.not_owner_token.key)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(obj.owner == self.not_owner)
