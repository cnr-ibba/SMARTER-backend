import json

from tests.base import BaseCase


class TestUserLogin(BaseCase):
    fixtures = ["user"]

    def test_successful_login(self):
        # Given
        username = "test"
        password = "password"
        payload = json.dumps({
            "username": username,
            "password": password
        })

        # When
        response = self.client.post(
            '/smarter-api/auth/login',
            headers={"Content-Type": "application/json"},
            data=payload)

        # Then
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)

    def test_login_with_invalid_user(self):
        # Given
        username = "another-user"
        password = "password"
        payload = json.dumps({
            "username": username,
            "password": password
        })

        # When
        response = self.client.post(
            '/smarter-api/auth/login',
            headers={"Content-Type": "application/json"},
            data=payload)

        # Then
        self.assertEqual(
            "Invalid username or password", response.json['message'])
        self.assertEqual(401, response.status_code)

    def test_login_with_invalid_password(self):
        # Given
        username = "test"
        password = "another-password"
        payload = json.dumps({
            "username": username,
            "password": password
        })

        # When
        response = self.client.post(
            '/smarter-api/auth/login',
            headers={"Content-Type": "application/json"},
            data=payload)

        # Then
        self.assertEqual(
            "Invalid username or password", response.json['message'])
        self.assertEqual(401, response.status_code)

    def test_login_with_missing_fields(self):
        # Given
        username = "test"
        payload = json.dumps({
            "username": username,
        })

        # When
        response = self.client.post(
            '/smarter-api/auth/login',
            headers={"Content-Type": "application/json"},
            data=payload)

        # Then
        self.assertEqual(
            "Request is missing required fields", response.json['message'])
        self.assertEqual(400, response.status_code)
