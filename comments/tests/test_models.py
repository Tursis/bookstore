import datetime

from django.test import TestCase

from comments.models import ProductReviews, ReviewComment
from test_unit_core.test_core import create_product_for_test, create_user

from profile.models import User

from store.models import Product, Book


class ProductReviewsModelTest(TestCase):
    def setUp(self):
        create_user('Test', '123456', 'test@gmail.com')
        create_user('Test2', '123456', 'test2@gmail.com')
        create_user('Test3', '123456', 'test3@gmail.com')
        create_product_for_test(2)

    def tearDown(self):
        for i in Product.objects.all():
            i.image.delete()

    def test_get_comments_counter(self):
        for item in [1, 2]:
            ProductReviews.objects.create(user=User.objects.get(pk=item), product=Product.objects.get(pk=item),
                                          description='Text comment %s' % item, rating=item,
                                          pub_date=datetime.datetime.now(), active=True)

        for item in [1, 2, 3, 4]:
            ReviewComment.objects.create(user=User.objects.get(pk=3), reviews=ProductReviews.objects.get(pk=1),
                                         comment='comment to review %s ' % item, pub_date=datetime.datetime.now(),
                                         active=True)

        for item in [1, 2, 3, 4, 5, 6]:
            ReviewComment.objects.create(user=User.objects.get(pk=3), reviews=ProductReviews.objects.get(pk=2),
                                         comment='comment to review %s ' % item, pub_date=datetime.datetime.now(),
                                         active=True)

        self.assertEqual(ProductReviews.objects.get(pk=1).get_comments_counter(), 4)
        self.assertEqual(ProductReviews.objects.get(pk=2).get_comments_counter(), 6)

