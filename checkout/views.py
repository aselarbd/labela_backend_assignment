from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.services import ShoppingCartManager
from checkout.serializers import CheckoutSerializer
from checkout.services import CheckoutService
from utils.logger import custom_logger

logger = custom_logger(__name__)

# Create your views here.


class CheckoutView(APIView):
    """Checkout items from shopping cart"""

    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSerializer

    @extend_schema(tags=["Checkout API"])
    def post(self, request: Request, *args, **kwargs):
        logger.info("CheckoutView checkout")
        user_id = request.user.id
        sopping_cart_manager = ShoppingCartManager()
        shopping_cart = sopping_cart_manager.get_shopping_cart(user_id=user_id)
        logger.debug("Getting shopping cart")

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            delivery_date = serializer.data.get("delivery_date")
            logger.debug("delivery_date is valid")

            order = CheckoutService.complete_order(
                delivery_date=delivery_date,
                shopping_cart=shopping_cart,
                user=request.user,
            )

            sopping_cart_manager.remove_shopping_cart(user_id=user_id)

            response = {
                "message": "checkout successfully",
                "order": order,
            }
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
