import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import CustomUser as User
from categories.models import Category, SubCategory
from products.models import Product, ProductVariant


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = User.objects.create_user(email='test@example.com', password='password123',
                                    first_name='Test', last_name='User')
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestOrderListCreateAPIView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, authenticated_client):
        self.api_client = api_client
        self.authenticated_client = authenticated_client

    def test_get_orders_unauthenticated(self):
        url = reverse('orders')
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_orders_authenticated(self):
        url = reverse('orders')
        response = self.authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_order_authenticated(self):

        url = reverse('orders')
        category = Category.objects.create(name="Electronics", description="Electronics Category")
        subcategory = SubCategory.objects.create(name="Mobile Phones", category=category)
        product = Product.objects.create(name="iPhone", description="iPhone 12", price=199,
                                         subcategory=subcategory,
                                         stock=10)
        variant = ProductVariant.objects.create(product=product, sku="12345", price=199, stock=5)

        data = {
            "items": [
                {
                    "variant_id": variant.id,
                    "quantity": 2,
                    "unit_price": 199
                }
            ],
            "total_price": 399,
            "status": "pending"
        }

        response = self.authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'pending'
