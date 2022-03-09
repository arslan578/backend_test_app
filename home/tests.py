from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.
from django.test import Client
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class ItemTest(TestCase):
    client = Client()
    """ Test module for Puppy model """

    def setUp(self):
        user = User(
            email="arslan@gmail.com", username="arslan!a")

        user.set_password('tester1234')
        user.save()


    def test_login_user(self):
        data = {
            'email': "arslan@gmail.com",
            "password": "tester1234"
        }
        response = self.client.post(path="/api/v1/login/", data=data)
        self.token = response.data['access_token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_items(self):
        login = {
            'email': "arslan@gmail.com",
            "password": "tester1234"
        }
        response = self.client.post(path="/api/v1/login/", data=login)
        token = response.data['access_token']
        data = {
            "items": {"data": [{"field_a": "aaa", "field_b": "bbbb"}]}
        }
        response = self.client.post(path='/api/v1/item/', data=data, HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, response.data)
