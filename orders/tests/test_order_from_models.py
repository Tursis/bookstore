from django.shortcuts import redirect

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from cart.models import Cart
from orders.forms import OrderCreateForm
from orders.models import Order, Purchase
from orders.order_from_models import OrderFromModels
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

    def test_add_to_order_from_model(self):
        form_data = {'first_name': 'name', 'last_name': 'last_name', 'email': 'test@gmail.com', 'address': 'test 10',
                     'postal_code': '1234', 'city': 'Test City'}
        form = OrderCreateForm(form_data)
        user = User.objects.get(pk=1)
        request = self.factory.post(redirect('order:order_view'))
        request.user = user
        Cart.objects.create(user=user, product=Product.objects.get(pk=1), quantity=5)
        Cart.objects.create(user=user, product=Product.objects.get(pk=2), quantity=3)
        order_from_model = OrderFromModels(request)
        order_from_model.add_to_order(form.save())
        self.assertTrue(Purchase.objects.all(), msg='Создан заказ')
        self.assertEqual(len(Purchase.objects.all()), 2, msg='Количество обьектов модели покупки должно быть 2')
        self.assertTrue(Order.objects.all(), msg='Создан заказ')
        self.assertEqual(len(Order.objects.all()), 1, msg='Количество заказов равно 1')
        self.assertEqual(Purchase.objects.get(pk=1).order, Order.objects.get(pk=1),
                         msg='Продукт с id=1 относиться к заказу с id=1')
        self.assertEqual(Purchase.objects.get(pk=2).order, Order.objects.get(pk=1),
                         msg='Продукт с id=2 относиться к заказу с id=1')
