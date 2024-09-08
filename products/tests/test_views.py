from decimal import Decimal
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from categories.models import Category, SubCategory
from products.models import Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = CustomUser.objects.create_user(email='test@example.com', first_name='Test',
                                          last_name='User', password='password123')
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def category():
    return Category.objects.create(name='Electronics', description='Electronic items')


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(category=category, name='Smartphones',
                                      description='All types of smartphones')


@pytest.fixture
def product(subcategory):
    return Product.objects.create(
        name='iPhone 13',
        description='Latest Apple smartphone',
        price=Decimal('999.99'),
        subcategory=subcategory,
        stock=10
    )


@pytest.mark.django_db
class TestProductListView:

    def test_get_products_unauthenticated(self, api_client, product):
        url = reverse('product-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'iPhone 13'

    def test_get_products_authenticated(self, authenticated_client, product):
        url = reverse('product-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'iPhone 13'


@pytest.mark.django_db
class TestProductBySubCategoryView:

    def test_get_products_by_subcategory_unauthenticated(self, api_client, subcategory, product):
        url = reverse('product-by-subcategory', kwargs={'subcategory_id': subcategory.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'iPhone 13'

    def test_get_products_by_subcategory_authenticated(self, authenticated_client, subcategory, product):
        url = reverse('product-by-subcategory', kwargs={'subcategory_id': subcategory.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'iPhone 13'

    def test_get_products_by_subcategory_not_found(self, api_client):
        url = reverse('product-by-subcategory', kwargs={'subcategory_id': 999})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == 'SubCategory not found'

    def test_post_product_unauthenticated(self, api_client, subcategory):
        url = reverse('product-by-subcategory', kwargs={'subcategory_id': subcategory.id})
        data = {'name': 'New Product', 'description': 'New product description', 'price': '199.99',
                'subcategory': subcategory.id, 'stock': 20}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_product_authenticated(self, authenticated_client, subcategory):
        url = reverse('product-by-subcategory', kwargs={'subcategory_id': subcategory.id})
        data = {'name': 'New Product', 'description': 'New product description', 'price': '199.99',
                'subcategory': subcategory.id, 'stock': 20}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Product'
        assert response.data['description'] == 'New product description'
        assert response.data['price'] == '199.99'
        assert response.data['subcategory'] == subcategory.id
        assert response.data['stock'] == 20

    def test_post_product_subcategory_not_found(self, authenticated_client):
        url = reverse('product-by-subcategory', kwargs={'subcategory_id': 999})
        data = {'name': 'New Product', 'description': 'New product description', 'price': '199.99', 'stock': 20}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == 'SubCategory not found'
