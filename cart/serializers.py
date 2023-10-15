from rest_framework import serializers
from product.models import Product


class CartSerializer(serializers.Serializer):
    product = serializers.IntegerField()

    def validate_product(self, value):
        product_exist = Product.objects.filter(id=value).exists()

        if not product_exist:
            raise serializers.ValidationError("Product must exist.")

        return value
