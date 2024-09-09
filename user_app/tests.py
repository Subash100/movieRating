from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegistrationTestCase(APITestCase):
    def test_register(self):
        data = {
            'username': 'testuser',
            'email':'testcase@example.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        }

        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(username='test',password='test')

    def test_login(self):
        url = reverse('login')
        data={
            'username':'test',
            'password':'test'
        }
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('logout')
        response=self.client.post(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)