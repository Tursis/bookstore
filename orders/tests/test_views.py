from unittest import mock

from django.urls import reverse

from django.shortcuts import redirect
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from cart.forms import CartAddProductForm
from cart.models import Cart
from orders.forms import OrderCreateForm
from store.models import Product
from test_unit_core.test_core import create_user, create_product_for_test


class OrderViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(5)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_url_redirect_create_order(self):
        resp = self.client.post(reverse('order:order_view'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'orders/create.html')

    def test_form_valid(self):
        form_data = {'first_name': 'name', 'last_name': 'last_name', 'email': 'test@gmail.com', 'address':'test 10', 'postal_code':'1234', 'city':'Test City'}
        form = OrderCreateForm(form_data)
        resp = self.client.post(reverse('order:order_view'))
        self.assertTrue(form.is_valid())
