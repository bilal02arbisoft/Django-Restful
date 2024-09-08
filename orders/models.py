from django.conf import settings
from django.db import models
from products.models import ProductVariant


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):

        return f"Order {self.id} - {self.user.first_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):

        return f"OrderItem {self.id} - Order {self.order.id}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity
