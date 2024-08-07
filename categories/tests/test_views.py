import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


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
