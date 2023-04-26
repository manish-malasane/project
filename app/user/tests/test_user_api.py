"""
Tests the user-API

- Endpoints
- 1) HTTP POST - /api/user/create/
- 2) HTTP POST - /api/user/token/   (PublicUserAPI)

- GET, PUT, PATCH - /api/user/me/ For valid credentials (PrivateUserAPI)


- Types of endpoints based on authorization
- public
- private
"""

from rest_framework.test import APITestCase, APIClient  # Either this
from django.test import TestCase, Client  # OR this both same
from django.shortcuts import reverse  # getting url associated with view
from django.contrib.auth import get_user_model  # django user model
from rest_framework import (
    status,
)  # getting Http status codes instead of hard-coding like 200,201,400, etc


# Named url of create view
CREATE_USER_URL = reverse("create")
TOKEN_URL = reverse("token")
ME_URL = reverse("me")


class TestsPublicUserAPI(TestCase):
    """
    Tests the public API endpoint from user API
    """

    @staticmethod
    def create_user(**params):
        """
        Return user
        """
        return get_user_model().objects.create_user(**params)

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
            "name": "Nathan",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, 201)

    def test_create_user_with_short_password(self):
        """
        Test error return if password is less than 5 characters
        """

        payload = {"email": "nathan5@gmail.com", "password": "qw", "name": "Nathan"}

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 400)

    def test_create_user_with_email_exists_error(self):
        """
        Test error return if user email already exists
        """

        payload = {
            "email": "nathan5@gmail.com",
            "password": "qwerty@123",
            "name": "Nathan",
        }

        self.create_user(**payload)  # creating user with payload

        # After creating user again try to create user on the server with same payload so, we will get 400
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, 400)

    def test_create_token_for_user(self):
        """
        Test generates a token for valid user credentials
        """

        payload = {
            "email": "manthan@gmail.com",
            "password": "manthan",
            "name": "Manthan",
        }

        # first create user with given payload
        # and then try to hit post request
        # If user with above payload credentials already exists no matter here we have to create user again for testcase
        self.create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_retrieve_user_unauthorised(self):
        """
        Test authentication is required for the user
        """

        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_bad_credentials(self):
        """
        Test return error if credentials are invalid
        """
        self.create_user(email="nathan@gmail.com", password="pass@123")
        payload = {"email": "nathan@gmail.com", "password": "qwert@123"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_email_not_found(self):
        """
        Test returns error if user n0t found with entered email
        """
        payload = {"email": "hughes@gmail.com", "password": "qwert@123"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """
        Test posting a blank password returns an error
        """

        payload = {"email": "steve@gmail.com", "password": ""}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class TestPrivateUserAPI(TestCase):
    """
    Test API requests which require authentication
    """

    @staticmethod
    def create_user(**params):
        return get_user_model().objects.create_user(**params)

    def setUp(self) -> None:
        self.client = APIClient()

        self.user = self.create_user(
            email="rahane@gmail.com", password="qwert@123", name="Rahane"
        )

        # We use force authenticate function for setting authentication flag as `True`
        # Wee don't need to create taken and authenticate each user under each test case
        # So we handled authentication by `force_authentication`
        # We don't need to create token and pass authorization header in request if `force_authenticate` is used
        # TODO - refer
        # https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile(self):
        """
        Test retrieving user info with valid token
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})

    def test_update_user_profile(self):
        """
        Test update user profile for an authenticated user
        """
        payload = {"email": "rohit@gmail.com", "name": "rohit sharma"}
        res = self.client.patch(ME_URL, payload)

        # To refresh the user old data with new data
        # whenever we hit any update request we have to do t
        # These method update new data with old data from database
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload.get("name"))
        self.assertEqual(self.user.email, payload.get("email"))

    def test_post_me_not_allowed(self):
        """
        Test POST-HTTP request is not allowed for
        `/api/user/me/`
        """

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
