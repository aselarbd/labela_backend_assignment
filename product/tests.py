from copy import deepcopy

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

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


class ProductListCreateTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = ProductListCreateView.as_view()
        self.url = reverse("product_list_create")

        # Create some initial posts
        Product.objects.create(
            name=SAMPLE_PRODUCT.get("name") + "_1",
            description=SAMPLE_PRODUCT.get("description") + "_1",
            price=SAMPLE_PRODUCT.get("price"),
            available_quantity=SAMPLE_PRODUCT.get("available_quantity"),
            active=SAMPLE_PRODUCT.get("active"),
        )
        Product.objects.create(
            name=SAMPLE_PRODUCT.get("name") + "_2",
            description=SAMPLE_PRODUCT.get("description") + "_2",
            price=SAMPLE_PRODUCT.get("price"),
            available_quantity=SAMPLE_PRODUCT.get("available_quantity"),
            active=SAMPLE_PRODUCT.get("active"),
        )

    def test_product_creation(self):
        sample_data = deepcopy(SAMPLE_PRODUCT)
        sample_data["name"] = SAMPLE_PRODUCT.get("name") + "_3"
        sample_data["description"] = SAMPLE_PRODUCT.get("description") + "_3"
        request = self.factory.post(self.url, sample_data)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], SAMPLE_PRODUCT.get("name") + "_3")
        self.assertEqual(
            response.data["description"], SAMPLE_PRODUCT.get("description") + "_3"
        )

    def test_list_products(self):
        request = self.factory.get(self.url)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], SAMPLE_PRODUCT.get("name") + "_1")
        self.assertEqual(response.data[1]["name"], SAMPLE_PRODUCT.get("name") + "_2")


class ProductRetrieveUpdateDeleteTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = ProductRetrieveUpdateDeleteView.as_view()
        self.product = Product.objects.create(
            name=SAMPLE_PRODUCT.get("name") + "_1",
            description=SAMPLE_PRODUCT.get("description") + "_1",
            price=SAMPLE_PRODUCT.get("price"),
            available_quantity=SAMPLE_PRODUCT.get("available_quantity"),
            active=SAMPLE_PRODUCT.get("active"),
        )
        self.url = reverse(
            "product_details_update_delete", kwargs={"pk": self.product.pk}
        )

    def test_get_product_by_id(self) -> None:
        request = self.factory.get(self.url)
        response = self.view(request, pk=self.product.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)
        self.assertEqual(response.data["description"], self.product.description)

    def test_update_product(self):
        updated_data = deepcopy(SAMPLE_PRODUCT)
        updated_data["name"] = SAMPLE_PRODUCT.get("name") + "_4"
        updated_data["description"] = SAMPLE_PRODUCT.get("description") + "_4"
        request = self.factory.put(self.url, updated_data, format="json")
        response = self.view(request, pk=self.product.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, SAMPLE_PRODUCT.get("name") + "_4")
        self.assertEqual(
            self.product.description, SAMPLE_PRODUCT.get("description") + "_4"
        )

    def test_delete_product(self):
        request = self.factory.delete(self.url)
        response = self.view(request, pk=self.product.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
