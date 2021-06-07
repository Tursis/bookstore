import datetime
from unittest import mock

from django.contrib.auth.models import User

from django.test import TestCase

from django.test.client import Client, RequestFactory
from django.urls import reverse

from comments.comments import add_product_reviews, quantity_reviews
from comments.forms import ProductReviewsForm
from comments.models import ProductReviews
from store.models import Product, Book
from test_unit_core.test_core import create_product_for_test, create_user


class CommentsFunctionTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        create_user('Test', '123456', 'test@gmail.com')
        create_user('Test2', '123456', 'test2@gmail.com')
        create_product_for_test(2)
        login = self.client.login(username='Tursis', password='123456')

    def tearDown(self):
        for i in Product.objects.all():
            i.image.delete()

    def test_add_product_reviews(self):
        for item in [1, 2]:
            user = User.objects.get(pk=item)
            product = Product.objects.get(pk=item)
            form_data = {'product': product.id, 'rating': 3 + item, 'description': 'Nice %s' % item}
            form = ProductReviewsForm(form_data)
            request = self.factory.post(reverse('reviews:product_reviews', args=(product.slug,)), form_data)
            request.user = user
            add_product_reviews(request, product.slug, form)
            self.assertEqual(ProductReviews.objects.get(pk=item).rating, 3 + item)
            self.assertEqual(ProductReviews.objects.get(pk=item).description, 'Nice %s' % item)
            self.assertEqual(ProductReviews.objects.get(pk=item).product, product)
        self.assertEqual(ProductReviews.objects.all().count(), 2)

    def test_quantity_reviews(self):
        for item in [1, 2]:
            ProductReviews.objects.create(user=User.objects.get(pk=item), product=Product.objects.get(pk=1),
                                          description='Text comment %s' % item, rating=item,
                                          pub_date=datetime.datetime.now(), active=True)
        self.assertEqual(quantity_reviews(Product.objects.get(pk=1).slug), 2)
