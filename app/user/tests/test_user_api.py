"""
Tests the user-API

- Endpoints
- 1) HTTP POST - /api/user/create/


- Types of endpoints based on authorization
- public
- private
"""

from rest_framework.test import APITestCase, APIClient  # Either this
from django.test import TestCase, Client                # OR this both same
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

# Named url of create view
CREATE_USER_URL = reverse("create")


class TestsPublicUserAPI(TestCase):
    """
    Tests the public API endpoint from user API
    """

    @staticmethod
    def create_user(**params):
        """
        Return user
        """
        return get_user_model().objects.create_user(
            **params
        )

    def setUp(self) -> None:
        """
        Instantiate Client
        """

        self.client = Client()

    def test_create_user_success(self):
        """
        Test creating user is successful
        (/api/user/create/)
        """

        payload = {
            "email": "nathan5@gmail.com",
            "password": "qwerty@123",
            "name": "Nathan"
        }

        res = self.client.post(CREATE_USER_URL,
                               payload)

        self.assertEqual(res.status_code, 201)

    def test_create_user_with_short_password(self):
        """
        Test error return if password is less than 5 characters
        """

        payload = {
            "email": "nathan5@gmail.com",
            "password": "qw",
            "name": "Nathan"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 400)

    def test_create_user_with_email_exists_error(self):
        """
        Test error return if user email already exists
        """

        payload = {
            "email": "nathan5@gmail.com",
            "password": "qwerty@123",
            "name": "Nathan"
        }

        self.create_user(**payload)  # creating user with payload

        # After creating user again try to create user on the server with same payload so, we will get 400
        res = self.client.post(CREATE_USER_URL,
                               payload)

        self.assertEqual(res.status_code, 400)
