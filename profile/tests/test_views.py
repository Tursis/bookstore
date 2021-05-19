from unittest import mock

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse


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
        print()
        user = get_user_model().objects.get(username='tursis')
        self.assertEqual(user.username, 'tursis')
        self.assertTrue(user.check_password(user_data['password1']))
        self.assertTrue(user.token)
        self.assertFalse(user.is_active)

    @mock.patch('profile.views.send_simple_message')
    def test_called_function_send_simple_message(self, mock_send_simple_message):
        user_data = {
            'username': 'tursis',
            'first_name': 'Oleh',
            'last_name': 'Spytsia',
            'email': 'oleh94@inbox.ru',
            'password1': 'Jktu199437',
            'password2': 'Jktu199437'
        }
        resp = self.client.post(reverse('profile:sign_up'), user_data)
        mock_send_simple_message.assert_called()

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


class ProfileDetailTest(TestCase):
    def setUp(self):
        # Создание двух пользователей
        test_user = User.objects.create_user(username='admin')
        test_user.set_password('admin')
        test_user.save()

    def test_redirect_if_user_no_login(self):
        resp = self.client.get(reverse('profile:profile_detail'))
        self.assertEqual(resp.status_code, 302)

    def test_profile_detail_page_url(self):
        login = self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('profile:profile_detail'))
        self.assertEqual(resp.status_code, 200)
        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'profile_detail.html')

    @mock.patch('profile.views.change_profile_data')
    @mock.patch('profile.views.change_profile_email')
    @mock.patch('profile.views.change_password')
    def test_called_function_profile_detail(self, mock_change_profile_data, mock_change_profile_email,
                                            mock_change_password):
        login = self.client.login(username='admin', password='admin')
        resp = self.client.post(reverse('profile:profile_detail'))
        mock_change_password.assert_called()
        mock_change_profile_data.assert_called()
        mock_change_profile_email.assert_called()

