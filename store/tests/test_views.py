from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from django.urls import reverse

from comments.models import ProductReviews
from store.models import Product
from test_unit_core.test_core import create_product_for_test, create_user


class ProductListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(2)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_index_template(self):
        resp = self.client.get(reverse('store:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    @mock.patch('store.views.ProductFilter')
    def test_call_product_filter(self, mock_product_filter):
        resp = self.client.get(reverse('store:index'))
        mock_product_filter.assert_called()

    @mock.patch('store.views.product_filter_counter')
    def test_call_product_filter_counter(self, mock_product_filter_counter):
        resp = self.client.get(reverse('store:index'))
        mock_product_filter_counter.assert_called()

    @mock.patch('store.views.update_model_counter')
    def test_call_update_model_counter(self, mock_update_model_counter):
        resp = self.client.get(reverse('store:index'))
        mock_update_model_counter.assert_called()


class BooksDetailView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(2)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_book_detail_template(self):
        product = Product.objects.get(pk=1)
        resp = self.client.get(reverse('store:book_detail', args=[product, ]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/book/book_detail.html')

    @mock.patch('store.views.quantity_reviews')
    def test_called_quantity_reviews(self, mock_quantity_reviews):
        product = Product.objects.get(pk=1)
        resp = self.client.get(reverse('store:book_detail', args=[product, ]))
        mock_quantity_reviews.assert_called()

    def test_product_reviews_form_in_context(self):
        product = Product.objects.get(pk=1)
        ProductReviews.objects.create(user=User.objects.get(pk=1), product=product, description='reviews', rating=4,
                                      active=True)
        resp = self.client.get(reverse('store:book_detail', args=[product, ]))
        self.assertTrue(resp.context['reviews_list'])

    def test_review_comment_form_in_context(self):
        product = Product.objects.get(pk=1)
        resp = self.client.get(reverse('store:book_detail', args=[product, ]))
        self.assertTrue(resp.context['comment_form'])


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
