from unittest import mock

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from django.urls import reverse

from store.models import Book, Magazine, Product, Category


class ProductReviewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create_user(username='Tursis')
        user.set_password('123456')
        user.email = 'test1@gmail.com'
        user.save()

        number_of_product = 13
        Category.objects.create(name='Книги')
        Category.objects.create(name='Журналы')

        for product_num in range(number_of_product):
            # Book.objects.create(category=Category.objects.get(pk=1), name='Book %s' % product_num, publisher='Издатель %s' % product_num,
            #                     price=product_num * 10, Discounts=0, author='Автор %s' % product_num,
            #                     genre='Жанр %s' % product_num, hard_cover='+', pages=5 * product_num,
            #                     pub_year=2000 + product_num, size='240x165')
            #
            # Magazine.objects.create(category=Category.objects.get(pk=2), name='Book %s' % product_num,
            #                         publisher='Издатель %s' % product_num,
            #                         price=product_num * 10, Discounts=0, numb=product_num, numb_in_year=product_num,
            #                         subs_price=20 * product_num, pages=5 * product_num,
            #                         pub_year=2000 + product_num, size='240x165')
            Product.objects.create(category=Category.objects.get(pk=1), name='Book %s' % product_num,
                                   slug='Book %s' % product_num, price=product_num * 10, Discounts=0, )
            Product.objects.create(category=Category.objects.get(pk=2), name='Magazine %s' % product_num,
                                   slug='Magazine %s' % product_num, price=product_num * 10, Discounts=0, )

    def test_product_reviews_url(self):
        login = self.client.login(username='Tursis', password='123456')

        product = Product.objects.get(pk=1)

        print(product)
        # resp = self.client.get(reverse('reviews:product_reviews', product.slug))
        # self.assertEqual(resp.status_code, 200)
        # # Проверка того, что мы используем правильный шаблон
        # self.assertTemplateUsed(resp, 'product_reviews.html')
