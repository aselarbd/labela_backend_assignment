from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.serializers import CartSerializer
from cart.services import ShoppingCartManager
from utils.logger import custom_logger

logger = custom_logger(__name__)

# Create your views here.


class CartRetrieveView(APIView):
    """View for get and shopping cart"""

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Cart API"])
    def get(self, request: Request, *args, **kwargs):
        logger.info("CartRetrieveView Get shopping cart")
        user_id = request.user.id
        sopping_cart_manager = ShoppingCartManager()
        shopping_cart = sopping_cart_manager.get_shopping_cart(user_id=user_id)
        logger.debug("Get shopping cart from manager")

        processed_shopping_cart = [
            shopping_cart.item_map[key] for key in shopping_cart.item_map
        ]

        return Response(data=processed_shopping_cart, status=status.HTTP_200_OK)


class AddCartView(APIView):
    """Add products to shopping cart"""

    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @extend_schema(tags=["Cart API"])
    def post(self, request: Request, *args, **kwargs):
        logger.info("AddCartView Add to shopping cart")
        user_id = request.user.id
        sopping_cart_manager = ShoppingCartManager()
        shopping_cart = sopping_cart_manager.get_shopping_cart(user_id=user_id)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            logger.debug("Product is validated")
            shopping_cart.add_product(product_id=serializer.data.get("product"))
            response = {"message": "product successfully added to shopping cart"}

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCartView(APIView):
    """Remove products from shopping cart"""

    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @extend_schema(tags=["Cart API"])
    def post(self, request: Request, *args, **kwargs):
        logger.info("RemoveCartView Remove from shopping cart")
        user_id = request.user.id
        sopping_cart_manager = ShoppingCartManager()
        shopping_cart = sopping_cart_manager.get_shopping_cart(user_id=user_id)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            logger.debug("Product is validated")
            remove_product = shopping_cart.remove_product(
                product_id=serializer.data.get("product")
            )
            if remove_product:
                response = {
                    "message": "product successfully removed from shopping cart"
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {"message": "product not exist in the shopping cart"}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
