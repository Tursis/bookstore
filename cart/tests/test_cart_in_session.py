from django.shortcuts import redirect
from django.test import TestCase

from django.test.client import Client, RequestFactory
from django.urls import reverse

from cart.cart_in_session import CartInSession
from store.models import Product, Book
from test_unit_core.test_core import create_product_for_test, create_user

PROFILE_DETAIL_URL = redirect('store:index')


def add_product_in_cart_session(self):
    product = Product.objects.get(pk=1)
    request = self.factory.post(PROFILE_DETAIL_URL)
    session = self.client.session
    request.session = session
    cart_manager = CartInSession(request)
    cart_manager.add(product.id, quantity=1)
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
        cart_manager = add_product_in_cart_session(self)
        self.assertTrue(cart_manager.cart)
        self.assertEqual(list(cart_manager.cart.keys())[0], product.id)
        self.assertEqual(list(cart_manager.cart.values())[0]['quantity'], 1)

    def test_remove_product_in_cart_session(self):
        # product = Product.objects.get(pk=1)
        # cart_manager = add_product_in_cart_session(self)
        product = Product.objects.get(pk=1)
        # request = self.factory.post(reverse('cart:cart_remove', args=(product.id,)), follow=True)
        request = self.factory.post(PROFILE_DETAIL_URL)
        session = self.client.session
        request.session = session
        cart_manager = CartInSession(request)
        cart_manager.add(product.id, quantity=1)



        print(cart_manager.__len__())
        cart_manager.remove(product)
        cart_manager.clear()

        print(cart_manager.cart)
        self.assertTrue(cart_manager.cart)

