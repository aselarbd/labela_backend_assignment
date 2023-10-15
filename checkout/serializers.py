from django.utils import timezone
from rest_framework import serializers


class CheckoutSerializer(serializers.Serializer):
    delivery_date = serializers.DateTimeField()

    def validate_delivery_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("delivery_date can't be a past date")
        return value
