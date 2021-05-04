from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Product, Book, Magazine
from django.urls import reverse


class ProductListViewTest(TestCase):

    @classmethod
    def SetUpTestData(cls):
        number_of_product = 13
        for product_num in range(number_of_product):
            Book.objects.create(category='Книги', name='Book %s' % product_num, publisher='Издатель %s' % product_num,
                                price=product_num * 10, Discounts=0, author='Автор %s' % product_num,
                                genre='Жанр %s' % product_num, hard_cover='+', pages=5 * product_num,
                                pub_year=2000 + product_num, size='240x165')

            Magazine.objects.create(category='Книги', name='Book %s' % product_num,
                                    publisher='Издатель %s' % product_num,
                                    price=product_num * 10, Discounts=0, numb=product_num, numb_in_year=product_num,
                                    subs_price=20 * product_num, pages=5 * product_num,
                                    pub_year=2000 + product_num, size='240x165')

    def test_get_response(self):
        resp = self.client.get('index.html')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('store:index'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'index.html')


class AuthorizationСheckTest(TestCase):

    def setUp(self):
        # Создание двух пользователей
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
