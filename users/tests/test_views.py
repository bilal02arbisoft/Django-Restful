from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class UsersListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@example.com', first_name='Test', last_name='User',
                                                   password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

    def test_get_users_list_authenticated(self):
        CustomUser.objects.create_user(email='test1@example.com', first_name='Test', last_name='User',
                                       password='password123')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_users_list_unauthenticated(self):
        self.client.credentials()
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SignupViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = '/api/auth/signup/'

    def test_signup(self):
        data = {
            'password': 'karachi123',
            'email': 'newuser@example.com',
            'first_name': 'new',
            'last_name': 'user',
            'profile': {
                'phone_number': '12345678901',
                'date_of_birth': '1990-01-01',
                'gender': 'M'
            }
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User created successfully')
        self.assertIn('user', response.data)
