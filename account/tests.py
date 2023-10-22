from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory

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
        account = User.objects.create(
            email="admin@auto.com",
            username="admin",
            password="admin",
            user_type=UserType.COMPANY.value,
        )
        self.assertEqual(account.username, "admin")
        self.assertEqual(account.email, "admin@auto.com")
        self.assertEqual(account.user_type, UserType.COMPANY.value)
        self.assertEqual(str(account), "( admin@auto.com )")

    def test_valid_signup_company(self):
        data = self._helper_generate_account_data(user_type=UserType.COMPANY.value)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "admin@auto.com")
        self.assertEqual(response.data["username"], "admin")
        self.assertEqual(response.data["user_type"], UserType.COMPANY.value)
        self.assertIn("token", response.data)

    def test_valid_signup_client(self):
        data = self._helper_generate_account_data(user_type=UserType.CLIENT.value)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_user_type_signup(self):
        data = self._helper_generate_account_data(user_type="CUSTOMER")
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="test",
            password="test",
            email="test@email.com",
            user_type=UserType.COMPANY.value,
        )
        self.url = reverse("logout")

    def test_logout_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Logged out successfully"})
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_without_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Token.objects.filter(user=self.user).exists())
