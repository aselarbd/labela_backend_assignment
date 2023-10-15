from product.models import Product


class ShoppingCart:
    """manage inside a shopping carts"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.item_map = {}

    def add_product(self, product_id: int) -> None:
        if product_id in self.item_map:
            item = self.item_map[product_id]
            item["quantity"] = item["quantity"] + 1
        else:
            product = Product.objects.filter(id=product_id).first()
            item = {"name": product.name, "product_id": product.id, "quantity": 1}
            self.item_map[product_id] = item

    def remove_product(self, product_id) -> bool:
        if product_id in self.item_map:
            item = self.item_map[product_id]
            if item["quantity"] == 1:
                del self.item_map[product_id]
            else:
                item["quantity"] = item["quantity"] - 1
            return True

        return False


class ShoppingCartManager:
    """Shopping cart manager manages all shopping carts"""

    SCM = {}

    def get_shopping_cart(self, user_id: int) -> ShoppingCart:
        """Get shopping cart. If shopping cart not exist, return empty cart"""

        if user_id not in self.SCM:
            self.SCM[user_id] = ShoppingCart(user_id=user_id)

        return self.SCM[user_id]

    def remove_shopping_cart(self, user_id: int) -> bool:
        """Remove shopping cart. If all things success, return True. If cart not exist, return false"""

        if user_id not in self.SCM:
            return False

        del self.SCM[user_id]
        return True
