from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from product.models import Product
from product.tests import _helper_create_user_account, _helper_create_product
from .services import ShoppingCart, ShoppingCartManager
from .views import CartRetrieveView, AddCartView, RemoveCartView


class TestShoppingCart(TestCase):
    def setUp(self):
        self.user = _helper_create_user_account()
        self.user_id = self.user.id
        self.product_mock = _helper_create_product(user=self.user, product_id=1)
        self.product_id = self.product_mock.id

        self.shopping_cart_manager = ShoppingCartManager()
        self.shopping_cart = self.shopping_cart_manager.get_shopping_cart(self.user_id)

    def tearDown(self):
        Product.objects.all().delete()
        self.shopping_cart.remove_product(product_id=self.product_id)
        self.shopping_cart_manager.SCM = {}

    def test_add_product(self):
        self.shopping_cart.add_product(self.product_id)
        self.assertIn(self.product_id, self.shopping_cart.item_map)
        self.shopping_cart.remove_product(self.product_id)

    def test_remove_product(self):
        self.shopping_cart.add_product(self.product_id)
        self.shopping_cart.remove_product(self.product_id)
        self.assertNotIn(self.product_id, self.shopping_cart.item_map)

    def test_calculate_total(self):
        self.shopping_cart = ShoppingCart(user_id=self.user_id)
        self.shopping_cart.add_product(self.product_id)
        total = self.shopping_cart.calculate_total()
        self.assertEqual(float(total), float(self.product_mock.price))
        self.shopping_cart.remove_product(self.product_id)

    def test_get_shopping_cart(self):
        cart = self.shopping_cart_manager.get_shopping_cart(self.user_id)
        self.assertIsInstance(cart, ShoppingCart)

    def test_remove_shopping_cart(self):
        self.shopping_cart_manager.remove_shopping_cart(self.user_id)
        self.assertNotIn(self.user_id, self.shopping_cart_manager.SCM)


class CartViewsTestCase(APITestCase):
    def setUp(self):
        self.user = _helper_create_user_account()
        self.user_id = self.user.id
        self.factory = APIRequestFactory()
        self.shopping_cart_manager = ShoppingCartManager()
        self.shopping_cart = self.shopping_cart_manager.get_shopping_cart(
            user_id=self.user_id
        )

    def test_cart_retrieve_view(self):
        url = reverse("get_shopping_cart")
        view = CartRetrieveView.as_view()
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_cart_view(self):
        url = reverse("add_shopping_cart")
        data = {"product": 1}
        view = AddCartView.as_view()
        request = self.factory.post(url, data=data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_cart_view(self):
        self.shopping_cart.add_product(1)
        url = reverse("remove_shopping_cart")
        data = {"product": 1}
        view = RemoveCartView.as_view()
        request = self.factory.post(url, data=data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"product": 2}
        view = RemoveCartView.as_view()
        request = self.factory.post(url, data=data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
