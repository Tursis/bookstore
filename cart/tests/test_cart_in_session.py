from django.shortcuts import redirect
from django.test import TestCase

from django.test.client import RequestFactory

from cart.cart_in_session import CartInSession
from store.models import Product, CategoryDiscount
from test_unit_core.test_core import create_product_for_test

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

    def test_get_total_price_category_discount_true(self):
        cart_manager = add_product_in_cart_session(self, 3)
        self.assertTrue(cart_manager.get_total_price())
        self.assertEqual(cart_manager.get_total_price(), 72)

    def test_get_total_price_category_discount_false(self):
        for category_discount in CategoryDiscount.objects.all():
            category_discount.active = False
            category_discount.save()
        cart_manager = add_product_in_cart_session(self, 3)
        self.assertTrue(cart_manager.get_total_price())
        self.assertEqual(cart_manager.get_total_price(), 80)

    def test_clear_cart_in_session(self):
        cart_manager = add_product_in_cart_session(self, 3)
        cart_manager.clear()
        self.assertFalse(cart_manager.session.keys())

    def test_cart_quantity_update(self):
        cart_manager = add_product_in_cart_session(self, 3)
        data = {'1': ['1'], '2': ['3'], '3': ['4']}
        request = self.factory.post(redirect('cart:cart_update'), data)
        cart_manager.cart_quantity_update(request.POST)
        self.assertEqual(cart_manager.cart['1']['quantity'], 1)
        self.assertEqual(cart_manager.cart['2']['quantity'], 3)
        self.assertEqual(cart_manager.cart['3']['quantity'], 4)
