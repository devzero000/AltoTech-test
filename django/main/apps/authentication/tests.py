from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APITestCase

from main.apps.users.factories import UserFactory


class AuthenticationTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api:token-auth')

        self.user = UserFactory(
            username='test',
            password=make_password('12345')  # NOSONAR
        )
        self.client.force_login(self.user)

    def test_token_auth(self):
        data = {
            'username': 'test',
            'password': '12345'  # NOSONAR
        }
        response = self.client.post(
            path=self.url,
            data=data,
            format='json',
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('refresh' in response_json)
        self.assertTrue('access' in response_json)
        self.assertEqual(response_json['user']['username'], 'test')
