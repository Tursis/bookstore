from unittest import mock

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from django.urls import reverse
from transliterate import slugify

from store.models import Book, Magazine, Product, Category, Publisher, BookAuthor, BookGenre


class ProductReviewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create_user(username='Tursis')
        user.set_password('123456')
        user.email = 'test1@gmail.com'
        user.save()

        number = 13
        [Category.objects.create(name=category_item) for category_item in range(1, 3)]
        [Publisher.objects.create(name=publisher_item) for publisher_item in range(1, number)]
        [BookAuthor.objects.create(name=author_item) for author_item in range(1, number)]
        [BookGenre.objects.create(name=genre_item) for genre_item in range(1, number)]

        for product_item in range(1, number):
            Book.objects.create(category=Category.objects.get(pk=1), name='book_%s' % product_item,
                                publisher=Publisher.objects.get(pk=product_item),
                                price=product_item * 10, Discounts=0, hard_cover='+', pages=5 * product_item,
                                pub_year=2000 + product_item, size='240x165'
                                )

            Book.objects.get(pk=product_item).author.add(BookAuthor.objects.get(pk=product_item))
            Book.objects.get(pk=product_item).genre.add(BookGenre.objects.get(pk=product_item))

        for product_item in range(1, number):
            Magazine.objects.create(category=Category.objects.get(pk=2), name='magazine_%s' % product_item,
                                    publisher=Publisher.objects.get(pk=product_item),
                                    price=product_item * 10, Discounts=0, numb=product_item, numb_in_year=product_item,
                                    subs_price=20 * product_item, pages=5 * product_item,
                                    pub_year=2000 + product_item, size='240x165')

    def test_product_reviews_url(self):
        login = self.client.login(username='Tursis', password='123456')
        product = Product.objects.get(pk=1)
        resp = self.client.post(reverse('reviews:product_reviews', args=(product.slug,)))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'product_reviews.html', product.slug)
