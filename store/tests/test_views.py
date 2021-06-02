from django.test import TestCase
from django.contrib.auth.models import User

from django.urls import reverse

from test_unit_core.test_core import create_product_for_test


class ProductListViewTest(TestCase):

    @classmethod
    def SetUpTestData(cls):
        create_product_for_test(2)

    def test_get_response(self):
        resp = self.client.get('index.html')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('store:index'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'index.html')


class AuthorizationСheckTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='admin')
        test_user.set_password('admin')
        test_user.is_superuser = True
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('store:product_manage'))
        self.assertRedirects(resp, '/accounts/login/?next=/store/manage/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('store:product_manage'))

        self.assertTrue(login)
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'store/product_manage.html')
