from rest_framework.test import APITestCase
from rest_framework import status

class UsersCreateAPIViewTest(APITestCase):
    def test_create_user(self, email):
        url = '/api/users/create/'
        data = {
            'username': 'testuser',
            'email': email,
            'password': 'testpassword',
        }
        if self.request.method == 'POST':
            email = self.request.POST
            if not email in '@gmail.com' or email in '@':
                return ValueError(status.HTTP_400_BAD_REQUEST,"Invalid email address in @ or @gmail.com")

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['username'], data['username'])
            self.assertEqual(response.data['email'], data['email'])