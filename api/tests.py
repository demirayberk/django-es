from typing import cast

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.settings import AUTH_SIGNATURE

User = get_user_model()


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = (  # pyright: ignore
            User.objects.create_user( # pyright: ignore
                username="test_user", password="test_password"
            ),
        )

    def test_login_view_valid_credentials(self):
        """Test login with valid credentials"""
        data = {"username": "test_user", "password": "test_password"}
        response = cast(
            Response, self.client.post("/api/auth/token/", data, format="json")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_view_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {"username": "test_user", "password": "asdasd"}
        response = cast(
            Response, self.client.post("/api/auth/token/", data, format="json")
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"error": "Invalid credentials"})


class ProtectedViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = (  # pyright: ignore
            User.objects.create_user(  # pyright: ignore
                username="test_user", password="test_password"
            ),
        )
        login_data = {"username": "test_user", "password": "test_password"}
        response = self.client.post("/api/auth/token/", login_data, format="json")
        self.token = response.data["token"]

    def test_protected_view_authenticated(self):
        headers = {"Authorization": f"{AUTH_SIGNATURE} {self.token}"}
        data = {"query": "some_query"}
        response = cast(
            Response,
            self.client.post("/api/search/", data, format="json", headers=headers),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total", container=response.data)
        self.assertIn("hits", container=response.data)

    def test_protected_view_unauthenticated(self):
        """Test access to protected view with invalid token"""
        headers = {"Authorization": f"{AUTH_SIGNATURE} asdasdasdasd"}
        data = {"query": "test_query"}
        response = self.client.post(
            "/api/search/", data, format="json", headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
