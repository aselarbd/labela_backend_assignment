from django.db import models
from account.models import User

# Create your models here.
from product.models import Product


class OrderSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateTimeField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order Summary - {self.user.email}"


class OrderDetails(models.Model):
    order = models.ForeignKey(OrderSummary, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order Details - {self.product.name} : {self.quantity}"
