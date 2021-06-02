from unittest import mock

from django.test import TestCase

from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from django.urls import reverse

from comments.forms import ProductReviewsForm
from store.models import Product
from test_unit_core.test_core import create_product_for_test


class ProductReviewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create_user(username='Tursis')
        user.set_password('123456')
        user.email = 'test1@gmail.com'
        user.save()
        login = self.client.login(username='Tursis', password='123456')
        create_product_for_test(2)

    def test_product_reviews_url(self):
        product = Product.objects.get(pk=1)
        resp = self.client.post(reverse('reviews:product_reviews', args=(product.slug,)), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'product_reviews.html', product.slug)

    @mock.patch('comments.views.add_product_reviews')
    def test_called_function_add_product_reviews(self, mock_add_product_reviews):
        product = Product.objects.get(pk=1)
        form_data = {'product': product.id, 'rating': 5, 'description': 'Nice'}
        resp = self.client.post(
            '/reviews/add/%s?next=/store/%s/%s' % (product.slug, product.category.slug, product.slug), form_data,
            follow=True)
        mock_add_product_reviews.assert_called()

    def test_redirect_back_to_product(self):
        product = Product.objects.get(pk=1)
        form_data = {'product': product.id, 'rating': 5, 'description': 'Nice'}
        form = ProductReviewsForm(form_data)
        resp = self.client.post(
            '/reviews/add/%s?next=/store/%s/%s' % (product.slug, product.category.slug, product.slug), form_data,
            follow=True)
        self.assertTrue(form.is_valid())
        self.assertRedirects(resp, ('/'), status_code=302, target_status_code=200)

    def test_redirect_if_user_no_login(self):
        self.client.logout()
        product = Product.objects.get(pk=1)
        resp = self.client.post(reverse('reviews:product_reviews', args=(product.slug,)))
        self.assertEqual(resp.status_code, 302)
