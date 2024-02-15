from django.test import TestCase
from django.urls import reverse


class TestUserCase(TestCase):

    def setUp(self):
        self.url_registration = reverse('main:register')
        self.user_data = {
            'username': 'user@mail.ru',
            'password1': 'Test77091',
            'password2': 'Test77091',
            'phone': "+79504455490",
            'nickname': 'Test nick',
            'first_name': 'Test Nick',
            'last_name': 'Test Nick'
        }

    def test_set_action_profile_object(self):
        """test for checking correctly registration new user"""
        # TODO set EMAIL SECRET KEY for uncomment test
        # response = self.client.post(self.url_registration, self.user_data)
        # response = response.json()
        # self.assertEqual(response['status'], 'success')

