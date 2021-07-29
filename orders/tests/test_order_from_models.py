from django.shortcuts import redirect

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from orders.forms import OrderCreateForm
from orders.models import Order, Purchase
from store.models import Product
from test_unit_core.test_core import create_user, create_product_for_test


class OrderFromSessionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(2)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_add_to_order_from_model(self):
        pass
