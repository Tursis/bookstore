from django.shortcuts import redirect
from django.test import TestCase

from django.test.client import Client, RequestFactory
from django.urls import reverse

from cart.cart_in_session import CartInSession
from store.models import Product, Book
from test_unit_core.test_core import create_product_for_test, create_user

PROFILE_DETAIL_URL = redirect('store:index')


class CartInSessionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        create_product_for_test(2)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_init_session(self):
        request = self.factory.post(PROFILE_DETAIL_URL)
        session = self.client.session
        request.session = session
        req = CartInSession(request)
        print(req.session)

        # self.assertEqual('c', 'cart')

    def test_add_product_in_session(self):
        pass
