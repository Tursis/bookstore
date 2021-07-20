from django.shortcuts import redirect
from django.test import TestCase

from django.test.client import Client, RequestFactory
from django.urls import reverse

from cart.cart_in_session import CartInSession
from store.models import Product, Book
from test_unit_core.test_core import create_product_for_test, create_user

PROFILE_DETAIL_URL = redirect('store:index')


def add_product_in_cart_session(self, quantity):
    request = self.factory.post(PROFILE_DETAIL_URL)
    session = self.client.session
    request.session = session
    cart_manager = CartInSession(request)
    for item in range(1, quantity + 1):
        product = Product.objects.get(pk=item)
        cart_manager.add(product.id, quantity=item)
    return cart_manager


class CartInSessionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        create_product_for_test(2)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_add_product_in_cart_session(self):
        product = Product.objects.get(pk=1)
        cart_manager = add_product_in_cart_session(self, 2)
        self.assertTrue(cart_manager.cart)
        self.assertEqual(list(cart_manager.cart.keys())[0], str(product.id))
        self.assertEqual(list(cart_manager.cart.values())[0]['quantity'], 1)

    def test_remove_product_in_cart_session(self):
        product = Product.objects.get(pk=1)
        cart_manager = add_product_in_cart_session(self, 1)
        cart_manager.remove(product.id)
        self.assertFalse(cart_manager.cart)

    def test_quantity_product_in_cart_session(self):
        cart_manager = add_product_in_cart_session(self, 3)
        self.assertEqual(cart_manager.__len__(), 6)

    def test_get_total_price(self):
        cart_manager = add_product_in_cart_session(self, 3)
        self.assertTrue(cart_manager.get_total_price())
        self.assertEqual(cart_manager.get_total_price(), 72)
