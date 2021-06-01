from io import BytesIO
from unittest import mock

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.test import TestCase

from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from django.urls import reverse

from comments.forms import ProductReviewsForm
from store.models import Book, Magazine, Product, Category, Publisher, BookAuthor, BookGenre


class ProductReviewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create_user(username='Tursis')
        user.set_password('123456')
        user.email = 'test1@gmail.com'
        user.save()
        login = self.client.login(username='Tursis', password='123456')

        number = 2
        [Category.objects.create(name=category_item) for category_item in ('Books', 'Magazine')]
        [Publisher.objects.create(name=publisher_item) for publisher_item in range(1, number)]
        [BookAuthor.objects.create(name=author_item) for author_item in range(1, number)]
        [BookGenre.objects.create(name=genre_item) for genre_item in range(1, number)]

        image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
        image_file = BytesIO(image.tobytes())
        file = InMemoryUploadedFile(image_file, None, 'test.jpg', 'image/jpg', 1024, None)

        for product_item in range(1, number):
            Book.objects.create(category=Category.objects.get(pk=1), name='book_%s' % product_item,
                                publisher=Publisher.objects.get(pk=product_item),
                                price=product_item * 10, Discounts=0, hard_cover='+', pages=5 * product_item,
                                pub_year=2000 + product_item, size='240x165', image=file
                                )

            Book.objects.get(pk=product_item).author.add(BookAuthor.objects.get(pk=product_item))
            Book.objects.get(pk=product_item).genre.add(BookGenre.objects.get(pk=product_item))
        for product_item in range(1, number):
            Magazine.objects.create(category=Category.objects.get(pk=2), name='magazine_%s' % product_item,
                                    publisher=Publisher.objects.get(pk=product_item),
                                    price=product_item * 10, Discounts=0, numb=product_item, numb_in_year=product_item,
                                    subs_price=20 * product_item, pages=5 * product_item,
                                    pub_year=2000 + product_item, size='240x165', image=file)

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
