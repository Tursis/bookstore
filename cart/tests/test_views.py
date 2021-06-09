from django.shortcuts import redirect
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

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
        resp = self.client.post('store/add/%s' % product.id)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('cart.html')

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