from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.eats.models import Place, User, Ingredient, Dish


class IngredientTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()

        self.token = Token.objects.get(user__username=user)

        self.ingredient = Ingredient.objects.create(name='test', calories=1)

        self.ingredient_instance = {'name': 'instance', 'calories': 5}

    def test_list_ingredients(self):
        """
        Test GET works without authorization
        """
        url = reverse('ingredients-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_ingredient(self):
        """
        Test GET (retrieve) works without authorization
        """
        url = reverse('ingredients-detail', args=(self.ingredient.id, ))

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ingredient(self):
        """
        Test POST with token returns 405
        """
        url = reverse('ingredients-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, self.ingredient_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_ingredient_without_token(self):
        """
        Test POST without token returns 401
        """
        url = reverse('ingredients-list')

        response = self.client.post(url, self.ingredient_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_ingredient(self):
        """
        Test PUT, PATCH with token returns 405
        """
        url = reverse('ingredients-detail', args=(self.ingredient.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, self.ingredient_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, self.ingredient_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_ingredient_without_token(self):
        """
        Test PUT, PATCH without token returns 401
        """
        url = reverse('ingredients-detail', args=(self.ingredient.id, ))

        response = self.client.put(url, self.ingredient_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(url, self.ingredient_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_ingredient(self):
        """
        Test DELETE with token returns 405
        """
        url = reverse('ingredients-detail', args=(self.ingredient.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url, self.ingredient_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_ingredient_without_token(self):
        """
        Test DELETE without token returns 401
        """
        url = reverse('ingredients-detail', args=(self.ingredient.id, ))

        response = self.client.delete(url, self.ingredient_instance, format='json')
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

        self.place = Place.objects.create(name='test', address='Moscow', owner=self.owner)
        self.place_instance = {'name': 'instance', 'address': 'Krasnoyarsk'}

    def test_list_places(self):
        """
        Test GET works without authorization
        """
        url = reverse('places-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_place(self):
        """
        Test GET (retrieve) works without authorization
        """
        url = reverse('places-detail', args=(self.place.id, ))

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
        url = reverse('places-detail', args=(self.place.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.place.owner == self.owner)

        response = self.client.patch(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.place.owner == self.owner)

    def test_update_not_owner_place(self):
        """
        Test PUT, PATCH with wrong owner token returns 403
        """
        url = reverse('places-detail', args=(self.place.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.not_owner_token.key)
        response = self.client.put(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.place.owner == self.not_owner)

        response = self.client.patch(url, self.place_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.place.owner == self.not_owner)

    def test_delete_place(self):
        """
        Test DELETE works only for owners of places
        """
        url = reverse('places-detail', args=(self.place.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.place.owner == self.owner)

    def test_delete_not_owner_place(self):
        """
        Test DELETE with wrong owner token returns 403
        """
        url = reverse('places-detail', args=(self.place.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.not_owner_token.key)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.place.owner == self.not_owner)


class DishTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(username='test')
        self.owner.set_password('test')
        self.owner.save()

        self.not_owner = User.objects.create(username='not_owner')
        self.not_owner.set_password('test')
        self.not_owner.save()

        self.token = Token.objects.get(user__username=self.owner)
        self.not_owner_token = Token.objects.get(user__username=self.not_owner)

        self.place = Place.objects.create(name='test', address='Moscow', owner=self.owner)

        self.ingredient = Ingredient.objects.create(name='test', calories=1)

        self.dish = Dish.objects.create(
            name='test',
            place=self.place,
            cost=1,
        )
        self.dish.ingredients.add(self.ingredient.id)
        self.dish.save()

        self.dish_instance = {
            'name': 'instance',
            'place': self.place.id,
            'cost': 1,
            'ingredients': (self.ingredient.id, ),
        }

    def test_list_dishes(self):
        """
        Test GET works without authorization
        """
        url = reverse('dishes-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_dish(self):
        """
        Test GET (retrieve) works without authorization
        """
        url = reverse('dishes-detail', args=(self.dish.id, ))

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_dish(self):
        """
        Test POST works only for owners of places
        """
        url = reverse('dishes-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, self.dish_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.place.owner == self.owner)

    def test_create_not_owner_dish(self):
        """
        Test POST doesn't with wrong owner token returns 403
        """
        url = reverse('dishes-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.not_owner_token.key)
        response = self.client.post(url, self.dish_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.place.owner == self.not_owner)

    def test_update_dish(self):
        """
        Test PUT, PATCH works only for owners of places
        """
        url = reverse('dishes-detail', args=(self.dish.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, self.dish_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.place.owner == self.owner)

        response = self.client.patch(url, self.dish_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.place.owner == self.owner)

    def test_update_not_owner_dish(self):
        """
        Test PUT, PATCH with wrong owner token returns 403
        """
        url = reverse('dishes-detail', args=(self.dish.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.not_owner_token.key)
        response = self.client.put(url, self.dish_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.place.owner == self.not_owner)

        response = self.client.patch(url, self.dish_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.place.owner == self.not_owner)

    def test_delete_dish(self):
        """
        Test DELETE works only for owners of places
        """
        url = reverse('dishes-detail', args=(self.dish.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.place.owner == self.owner)

    def test_delete_not_owner_dish(self):
        """
        Test DELETE with wong owner token returns 403
        """
        url = reverse('dishes-detail', args=(self.dish.id, ))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.not_owner_token.key)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.place.owner == self.not_owner)
