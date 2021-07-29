from django.shortcuts import redirect

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from orders.forms import OrderCreateForm
from orders.models import Order, Purchase
from orders.order_from_session import OrderFromSession
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

    def test_add_to_order_from_session(self):
        session = self.client.session
        form_data = {'first_name': 'name', 'last_name': 'last_name', 'email': 'test@gmail.com', 'address': 'test 10',
                     'postal_code': '1234', 'city': 'Test City'}
        form = OrderCreateForm(form_data)
        request = self.factory.post(redirect('order:order_view'))
        request.user = User.objects.get(pk=1)
        request.session = session
        cart = session['cart'] = {}
        cart[str(Product.objects.get(pk=1).id)] = {'quantity': 3}
        cart[str(Product.objects.get(pk=2).id)] = {'quantity': 2}
        order_from_session = OrderFromSession(request)
        order_from_session.add_to_order(form.save())
        self.assertEqual(len(Purchase.objects.all()), 2, msg='Количество обьектов модели покупки должно быть 2')
        self.assertTrue(Order.objects.all(), msg='Создан заказ')
        self.assertEqual(len(Order.objects.all()), 1, msg='Количество заказов равно 1')
        self.assertEqual(Purchase.objects.get(pk=1).order, Order.objects.get(pk=1),
                         msg='Продукт с id=1 относиться к заказу с id=1')
        self.assertEqual(Purchase.objects.get(pk=2).order, Order.objects.get(pk=1),
                         msg='Продукт с id=2 относиться к заказу с id=1')
