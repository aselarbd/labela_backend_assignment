from copy import deepcopy

from checkout.models import OrderSummary, OrderDetails
from product.models import Product


class CheckoutService:
    @staticmethod
    def complete_order(delivery_date, shopping_cart, user) -> dict:
        total = shopping_cart.calculate_total()

        order_summary = OrderSummary(
            user=user, total=total, delivery_date=delivery_date
        )
        order_summary.save()

        for _, item in shopping_cart.item_map.items():
            product = Product.objects.get(id=item["product_id"])
            order_details = OrderDetails(
                order=order_summary, product=product, quantity=item["quantity"]
            )
            order_details.save()

        order = deepcopy(
            {
                "order_id": order_summary.id,
                "order_total": total,
                "delivery_date": delivery_date,
                "products": [
                    shopping_cart.item_map[key] for key in shopping_cart.item_map
                ],
            }
        )

        return order
