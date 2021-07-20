from unittest import mock

from django.test import TestCase

from django.test.client import Client, RequestFactory
from django.urls import reverse

from comments.forms import ProductReviewsForm
from store.models import Product, Book, Magazine
from test_unit_core.test_core import create_product_for_test, create_user


class ProductReviewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(2)
        login = self.client.login(username='Tursis', password='123456')

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

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


class ReviewCommentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(2)
        login = self.client.login(username='Tursis', password='123456')

    def tearDown(self):
        for i in Product.objects.all():
            i.image.delete()

    def test_book_detail_url(self):
        book = Book.objects.get(pk=1)
        resp = self.client.post(reverse('store:book_detail', args=(book.slug,)), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/book/book_detail.html', book.slug)

    def test_magazine_detail_url(self):
        magazine = Magazine.objects.get(pk=3)
        resp = self.client.post(reverse('store:magazine_detail', args=(magazine.slug,)), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/magazine/magazine_detail.html', magazine.slug)

    @mock.patch('comments.views.add_review_comment')
    def test_called_function_add_review_comment(self, mock_add_review_comment):
        product = Product.objects.get(pk=1)
        form_data = {'comment': 'Nice'}
        resp = self.client.post(reverse('store:book_detail', args=(product.slug,)), form_data)
        mock_add_review_comment.assert_called()

    @mock.patch('comments.views.add_review_comment')
    def test_access_to_add_review_comment_if_user_no_login(self, mock_add_review_comment):
        self.client.logout()
        product = Product.objects.get(pk=1)
        form_data = {'comment': 'Nice'}
        resp = self.client.post(reverse('store:book_detail', args=(product.slug,)), form_data)
        self.assertEqual(resp.status_code, 302)
