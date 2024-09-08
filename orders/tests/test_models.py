import pytest
from django.core.exceptions import ValidationError
from users.models import CustomUser as User
from orders.models import Order, OrderItem
from products.models import Product, ProductVariant
from categories.models import Category, SubCategory


@pytest.mark.django_db
class TestOrderModels:

    def test_create_order(self):
        user = User.objects.create_user(email='test@example.com', password='password123',
                                        first_name='new', last_name='user')
        order = Order.objects.create(user=user, total_price=100.00)
        assert order.user == user
        assert order.status == 'pending'
        assert order.total_price == 100.00
        assert str(order) == f"Order {order.id} - {user.first_name}"

    def test_create_order_item(self):
        user = User.objects.create_user(email='test@example.com', password='password123',
                                        first_name='new', last_name='user')
        category = Category.objects.create(name="Electronics", description="Electronics Category")
        subcategory = SubCategory.objects.create(name="Mobile Phones", category=category)
        product = Product.objects.create(name="iPhone", description="iPhone 12",
                                         price=999.99, subcategory=subcategory, stock=10)
        variant = ProductVariant.objects.create(product=product, sku="12345", price=999.99, stock=5)
        order = Order.objects.create(user=user, total_price=100.00)
        order_item = OrderItem.objects.create(order=order, variant=variant, quantity=2, unit_price=999.99)
        assert order_item.order == order
        assert order_item.variant == variant
        assert order_item.quantity == 2
        assert order_item.unit_price == 999.99
        assert order_item.total_price == 1999.98
        assert str(order_item) == f"OrderItem {order_item.id} - Order {order.id}"

    def test_order_status_choices(self):
        user = User.objects.create_user(email='test@example.com', password='password123',
                                        first_name='new', last_name='user')
        order = Order.objects.create(user=user, total_price=100.00)
        order.status = 'shipped'
        order.save()
        assert order.status == 'shipped'
        order.status = 'delivered'
        order.save()
        assert order.status == 'delivered'
        order.status = 'cancelled'
        order.save()
        assert order.status == 'cancelled'
        with pytest.raises(ValidationError):
            order.status = 'invalid_status'
            order.full_clean()
