from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from utils.user_types import UserType


class SignUpViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("signup")

    @staticmethod
    def _helper_generate_account_data(user_type) -> dict:
        return {
            "email": "admin@auto.com",
            "username": "admin",
            "password": "admin",
            "user_type": user_type,
        }

    def test_account_model(self):
        account = User.objects.create(email="admin@auto.com", username="admin", password="admin", user_type=UserType.COMPANY.value)
        self.assertEqual(account.username, "admin")
        self.assertEqual(account.email, "admin@auto.com")
        self.assertEqual(account.user_type, UserType.COMPANY.value)
        self.assertEqual(str(account), "( admin@auto.com )")

    def test_valid_signup_company(self):
        data = self._helper_generate_account_data(user_type=UserType.COMPANY.value)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_signup_client(self):
        data = self._helper_generate_account_data(user_type=UserType.CLIENT.value)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_user_type_signup(self):
        data = self._helper_generate_account_data(user_type='CUSTOMER')
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
