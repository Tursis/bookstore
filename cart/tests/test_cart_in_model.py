from itertools import count

from django.shortcuts import redirect
from django.test import TestCase

from django.contrib.auth.models import User

from django.test.client import Client, RequestFactory
from django.urls import reverse

from cart.cart_in_model import CartInModel
from cart.cart_in_session import CartInSession
from cart.models import Cart
from store.models import Product, CategoryDiscount
from test_unit_core.test_core import create_product_for_test, create_user

PROFILE_DETAIL_URL = redirect('store:index')


def add_product_in_cart_model(self, user, product_id, quantity):
    request = self.factory.post(PROFILE_DETAIL_URL)
    request.user = user
    request.session = self.client.session
    cart_manager = CartInModel(request)
    product = Product.objects.get(pk=product_id)
    cart_manager.add(product.id, quantity)
    return cart_manager


class CartInModelTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        create_user('Test', '123456', 'test@gmail.com')
        create_user('Test2', '123456', 'test@gmail2.com')
        create_product_for_test(3)
        login = self.client.login(username='Test', password='123456')

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_init_cart_in_model_if_cart_in_session_not_empty(self):
        user = User.objects.get(pk=1)
        request = self.factory.post(PROFILE_DETAIL_URL)
        request.user = user
        request.session = self.client.session
        cart_in_session = CartInSession(request)
        product = Product.objects.get(pk=1)
        cart_in_session.add(product.id, quantity=2)
        cart_in_model = CartInModel(request)
        self.assertTrue(Cart.objects.all(), msg='Перенос корзины товара из сесии в модель')

    def test_add_product_in_cart_model(self):
        user = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        cart_manager = add_product_in_cart_model(self, user, product_id=1, quantity=3)
        cart_manager = add_product_in_cart_model(self, user, product_id=2, quantity=2)
        cart_manager = add_product_in_cart_model(self, user, product_id=3, quantity=2)
        cart_manager = add_product_in_cart_model(self, user2, product_id=1, quantity=4)
        cart_manager = add_product_in_cart_model(self, user2, product_id=3, quantity=4)
        self.assertEqual(len(Cart.objects.all()), 5, msg='Количество экземпляров корзины должно быть 5')
        self.assertEqual(len(Cart.objects.filter(user=user)), 3,
                         msg='Количетсво экземпляров корзины пользователя Test должен быть 3')

    def test_remove_product_in_cart_model(self):
        user = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        cart_manager_user = add_product_in_cart_model(self, user, product_id=1, quantity=1)
        cart_manager_user = add_product_in_cart_model(self, user, product_id=2, quantity=2)
        cart_manager_user2 = add_product_in_cart_model(self, user2, product_id=1, quantity=4)

        product = Product.objects.get(pk=1)
        cart_manager_user.remove(product)
        self.assertEqual(len(Cart.objects.filter(user=user)), 1,
                         msg='После удаления одного товара у пользователя Test остаеться один товар')
        self.assertEqual(len(Cart.objects.filter(user=user2)), 1,
                         msg='После удаления одного товара у пользователя Test у пользователя Test2 остаеться товар')
        cart_manager_user2.remove(product)
        self.assertEqual(len(Cart.objects.filter(user=user2)), 0,
                         msg='После удаления одного товара у пользователя Test2 остаеться пустая корзина')


