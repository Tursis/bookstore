from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.status import HTTP_400_BAD_REQUEST


class SignUpViewTest(TestCase):
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
