from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SignUpViewTestCase(APITestCase):
    def test_valid_signup_company(self):
        url = reverse("signup")
        data = {
            "email": "admin@auto.com",
            "username": "admin",
            "password": "admin",
            "user_type": "COMPANY",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_signup_client(self):
        url = reverse("signup")
        data = {
            "email": "user@auro.com",
            "username": "user",
            "password": "user",
            "user_type": "CLIENT",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_user_type_signup(self):
        url = reverse("signup")
        data = {
            "email": "test@auto.com",
            "username": "test",
            "password": "test",
            "user_type": "CUSTOMER",  # Use an invalid user type
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
