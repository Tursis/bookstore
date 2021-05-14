from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.status import HTTP_400_BAD_REQUEST

from profile.models import Token

class SignUpViewRedirectTest(TestCase):
    def setUp(self):
        # Создание двух пользователей
        test_user = User.objects.create_user(username='admin')
        test_user.set_password('admin')
        test_user.is_superuser = True
        test_user.save()

    def test_redirect_if_user_login(self):
        login = self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('profile:sign_up'))
        self.assertTrue(login)
        self.assertEqual(resp.status_code, 302)

    def test_signup_page_url(self):
        resp = self.client.get(reverse('profile:sign_up'))
        self.assertEqual(resp.status_code, 200)
        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'registration/sign_up.html')


class SignUpViewTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_create_user(self):
        user_data = {
            'username': 'tursis',
            'first_name': 'Oleh',
            'last_name': 'Spytsia',
            'email': 'oleh94@inbox.ru',
            'password1': 'Jktu199437',
            'password2': 'Jktu199437'
        }
        resp = self.client.post(reverse('profile:sign_up'), user_data)
        user = get_user_model().objects.get(username='tursis')
        self.assertEqual(user.username, 'tursis')
        self.assertTrue(user.check_password(user_data['password1']))
        self.assertTrue(user.token)
        self.assertFalse(user.is_active)

    def test_activate_account(self):
        user_data = {
            'username': 'tursis',
            'first_name': 'Oleh',
            'last_name': 'Spytsia',
            'email': 'oleh94@inbox.ru',
            'password1': 'Jktu199437',
            'password2': 'Jktu199437'
        }
        resp = self.client.post(reverse('profile:sign_up'), user_data, follow=True)
        user = get_user_model().objects.get(pk=1)
        resp = self.client.get(reverse('profile:activate_account', kwargs={'token': user.token.token}), follow=True)
        user = get_user_model().objects.get(pk=1)
        self.assertTemplateUsed(resp, 'registration/account_activation_email.html')
        self.assertTrue(user.is_active)

