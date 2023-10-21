from copy import deepcopy

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from account.models import User
from utils.user_types import UserType
from .models import Product
from .views import ProductListCreateView, ProductRetrieveUpdateDeleteView
from django.urls import reverse

# Create your tests here.

SAMPLE_PRODUCT = {
    "name": "Test product",
    "description": "Test description",
    "price": 12.99,
    "available_quantity": 40,
    "active": True,
}


def _helper_create_user_account():
    return User.objects.create_user(
        username="test",
        password="test",
        email="test@email.com",
        user_type=UserType.COMPANY.value,
    )


def _helper_create_product(user: User, product_id: int):
    return Product.objects.create(
        name=f"Test product {product_id}",
        description=f"Test description {product_id}",
        price=12.99,
        available_quantity=40,
        active=True,
        created_by=user,
    )


class ProductListCreateTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = ProductListCreateView.as_view()
        self.url = reverse("product_list_create")
        self.user = _helper_create_user_account()

        # Create some initial products
        _helper_create_product(user=self.user, product_id=1)
        _helper_create_product(user=self.user, product_id=2)

    def test_product_creation(self):
        sample_data = deepcopy(SAMPLE_PRODUCT)
        request = self.factory.post(self.url, data=sample_data, format="json")
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], sample_data.get("name"))
        self.assertEqual(response.data["description"], sample_data.get("description"))

    def test_list_products(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductRetrieveUpdateDeleteTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = ProductRetrieveUpdateDeleteView.as_view()
        self.user = _helper_create_user_account()
        self.product = _helper_create_product(user=self.user, product_id=1)

        self.url = reverse(
            "product_details_update_delete", kwargs={"pk": self.product.pk}
        )

    def test_product_model(self):
        self.assertEqual(self.product.name, "Test product 1")
        self.assertEqual(self.product.description, "Test description 1")
        self.assertEqual(self.product.created_by.username, self.user.username)

    def test_get_product_by_id(self) -> None:
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)
        self.assertEqual(response.data["description"], self.product.description)

    def test_update_product(self):
        updated_data = deepcopy(SAMPLE_PRODUCT)
        updated_name = "Updated name"
        updated_description = "Updated description"
        updated_data["name"] = updated_name
        updated_data["description"] = updated_description

        request = self.factory.put(self.url, updated_data, format="json")
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, updated_name)
        self.assertEqual(self.product.description, updated_description)

    def test_delete_product(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
