from django.test import TestCase

from orders.models import Order, Purchase
from orders.orders import get_total_price
from store.models import Product
from test_unit_core.test_core import create_user, create_product_for_test


class OrderTest(TestCase):
    def setUp(self):
        create_user('Tursis', '123456', 'test@gmail.com')
        create_product_for_test(5)

    def tearDown(self):
        for item in Product.objects.all():
            item.image.delete()

    def test_get_total_price(self):
        Order.objects.create(first_name='Test name', last_name='Test last name', email='test@gmail.com',
                             address='test address', postal_code='test code', city='test city', paid=False)

        Purchase.objects.create(order=Order.objects.get(pk=1), product=Product.objects.get(pk=1),
                                price=Product.objects.get(pk=1).price, quantity=2)

        Purchase.objects.create(order=Order.objects.get(pk=1), product=Product.objects.get(pk=2),
                                price=Product.objects.get(pk=2).price, quantity=1)

        purchase = Purchase.objects.filter(order=Order.objects.get(pk=1))
        self.assertEqual(get_total_price(purchase), 36, msg='Сума заказа должна быть 36')
