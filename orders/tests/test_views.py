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


def order_create_form_for_test():
    form_data = {'first_name': 'name', 'last_name': 'last_name', 'email': 'test@gmail.com', 'address': 'test 10',
                 'postal_code': '1234', 'city': 'Test City'}
    form = OrderCreateForm(form_data)
    return form


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
        self.assertEqual(resp.status_code, 200, msg='Страница должна загрузиться с кодом 200')
        self.assertTemplateUsed(resp, 'orders/create.html')

    def test_form_valid(self):
        form = order_create_form_for_test()
        resp = self.client.post(reverse('order:order_view'))
        self.assertTrue(form.is_valid(), msg='Проверка валидности формы заполнения заказа')

    @mock.patch('orders.views.OrdersCreate.add_to_order')
    def test_call_method_add_to_order(self, mock_add_to_order):
        form = order_create_form_for_test()
        resp = self.client.post(reverse('order:order_view'), form.data)
        mock_add_to_order.assert_called()

    @mock.patch('orders.views.get_total_price')
    def test_call_get_total_price(self, mock_get_total_price):
        form = order_create_form_for_test()
        resp = self.client.post(reverse('order:order_view'), form.data)
        mock_get_total_price.assert_called()

    @mock.patch('orders.views.send_simple_message')
    def test_call_send_simple_message(self, mock_send_simple_message):
        form = order_create_form_for_test()
        resp = self.client.post(reverse('order:order_view'), form.data)
        mock_send_simple_message.assert_called()

