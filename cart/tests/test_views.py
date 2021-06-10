from unittest import mock

from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient

from django.shortcuts import redirect
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from cart.forms import CartAddProductForm
from cart.models import Cart
from store.models import Product
from test_unit_core.test_core import create_user, create_product_for_test


class СartAddViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(2)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_redirect_add_cart(self):
        product = Product.objects.get(pk=1)
        user = User.objects.get(pk=1)
        resp = self.client.post(reverse('cart:cart_add', args=(product.id,)), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('cart.html')

    @mock.patch('cart.views.CartManager.add')
    def test_called_add_cart(self, mock_cart_manage_add):
        product = Product.objects.get(pk=1)
        user = User.objects.get(pk=1)
        form_data = {'update': False}
        form = CartAddProductForm(form_data)
        resp = self.client.post(reverse('cart:cart_add', args=(product.id,)), form_data, follow=True)
        self.assertTrue(form.is_valid())
        mock_cart_manage_add.assert_called()

    def test_redirect_remove_cart(self):
        product = Product.objects.get(pk=1)
        resp = self.client.post('store/remove/%s' % product.id)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('cart.html')

    def test_cart_url(self):
        login = self.client.login(username='Tursis', password='123456')
        product = Product.objects.get(pk=1)
        user = User.objects.get(pk=1)
        Cart.objects.create(user=user, product=product, quantity=5)
        cart = Cart.objects.filter(user=user)
        resp = self.client.post(redirect('cart:cart_detail'), {'cart': cart})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('cart.html')

    def test_cart_update(self):
        # login = self.client.login(username='Tursis', password='123456')
        # user = User.objects.get(pk=1)
        # factory = APIRequestFactory()
        resp = self.client.post(redirect('cart:cart_update'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('cart.html')
