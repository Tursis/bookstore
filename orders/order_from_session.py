from django.shortcuts import render
from cart.cart_in_session import CartInSession
from .models import Purchase, Product
from .forms import OrderCreateForm


class OrderFromSession:
    """
    Перенос даних корзины из сесии в заказ.
    """
    def __init__(self, request):
        self.cart = CartInSession(request)
        self.purchase = Purchase()

    def add_to_order(self, request, order):
        for item in self.cart:
            product = Product.objects.get(name=item['product'])
            Purchase.objects.create(order=order,
                                    product=item['product'],
                                    price=product.price,
                                    quantity=item['quantity'])
            # очистка корзины
        self.cart.clear()
