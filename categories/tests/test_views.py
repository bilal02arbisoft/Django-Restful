import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from categories.models import Category, SubCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = CustomUser.objects.create_user(email='test@example.com', first_name='Test', last_name='User', password='password123')
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

@pytest.mark.django_db
class TestCategoryListCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, authenticated_client):
        self.api_client = api_client
        self.authenticated_client = authenticated_client

    def test_get_categories_unauthenticated(self):
        url = reverse('categories_list_create')
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_categories_authenticated(self):
        url = reverse('categories_list_create')
        response = self.authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_category_unauthenticated(self):
        url = reverse('categories_list_create')
        data = {'name': 'New Category', 'description': 'New Category Description'}
        response = self.api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_category_authenticated(self):
        url = reverse('categories_list_create')
        data = {'name': 'New Category', 'description': 'New Category Description'}
        response = self.authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Category'
        assert response.data['description'] == 'New Category Description'
#
# @pytest.mark.django_db
# class TestCategoryDetailUpdateView:
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, authenticated_client):
#         self.api_client = api_client
#         self.authenticated_client = authenticated_client
#         self.category = Category.objects.create(name='Electronics', description='Electronic items')
#
#     def test_get_category_unauthenticated(self):
#         url = reverse('category-detail-update', kwargs={'pk': self.category.pk})
#         response = self.api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['name'] == 'Electronics'
#
#     def test_get_category_authenticated(self):
#         url = reverse('category-detail-update', kwargs={'pk': self.category.pk})
#         response = self.authenticated_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['name'] == 'Electronics'
#
#     def test_put_category_unauthenticated(self):
#         url = reverse('category-detail-update', kwargs={'pk': self.category.pk})
#         data = {'name': 'Updated Electronics', 'description': 'Updated description'}
#         response = self.api_client.put(url, data, format='json')
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_put_category_authenticated(self):
#         url = reverse('category-detail-update', kwargs={'pk': self.category.pk})
#         data = {'name': 'Updated Electronics', 'description': 'Updated description'}
#         response = self.authenticated_client.put(url, data, format='json')
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['name'] == 'Updated Electronics'
#         assert response.data['description'] == 'Updated description'
#
# @pytest.mark.django_db
# class TestSubCategoryByCategoryListCreateView:
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, authenticated_client):
#         self.api_client = api_client
#         self.authenticated_client = authenticated_client
#         self.category = Category.objects.create(name='Electronics', description='Electronic items')
#
#     def test_get_subcategories_unauthenticated(self):
#         subcategory = SubCategory.objects.create(category=self.category, name='Smartphones', description='All types of smartphones')
#         url = reverse('subcategory-by-category-list-create', kwargs={'category_id': self.category.pk})
#         response = self.api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]['name'] == 'Smartphones'
#
#     def test_get_subcategories_authenticated(self):
#         subcategory = SubCategory.objects.create(category=self.category, name='Smartphones', description='All types of smartphones')
#         url = reverse('subcategory-by-category-list-create', kwargs={'category_id': self.category.pk})
#         response = self.authenticated_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]['name'] == 'Smartphones'
#
#     def test_post_subcategory_unauthenticated(self):
#         url = reverse('subcategory-by-category-list-create', kwargs={'category_id': self.category.pk})
#         data = {'name': 'Laptops', 'description': 'All types of laptops'}
#         response = self.api_client.post(url, data, format='json')
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_post_subcategory_authenticated(self):
#         url = reverse('subcategory-by-category-list-create', kwargs={'category_id': self.category.pk})
#         data = {'name': 'Laptops', 'description': 'All types of laptops'}
#         response = self.authenticated_client.post(url, data, format='json')
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['name'] == 'Laptops'
#         assert response.data['description'] == 'All types of laptops'
#
# @pytest.mark.django_db
# class TestSubCategoryListView:
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client):
#         self.api_client = api_client
#         self.category = Category.objects.create(name='Electronics', description='Electronic items')
#
#     def test_get_subcategories(self):
#         SubCategory.objects.create(category=self.category, name='Smartphones', description='All types of smartphones')
#         url = reverse('subcategory-list')
#         response = self.api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]['name'] == 'Smartphones'
