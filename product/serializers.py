from rest_framework import serializers
from .models import Product


class ProductDetailsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = serializers.IntegerField(default=0)
    active = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "available_quantity",
            "active",
            "created",
        ]

    def validate_available_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("quantity can't be negative")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]
