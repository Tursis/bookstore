from django.shortcuts import render
from cart.cart_in_session import CartInSession
from .models import Purchase, Product
from .forms import OrderCreateForm


class OrderFromSession:
    def __init__(self, request):
        self.cart = CartInSession(request)
        self.purchase = Purchase()

    def add_to_order(self, request, order):
        for item in self.cart:
            Purchase.objects.create(order=order,
                                    product=item['product'],
                                    price=2,
                                    quantity=item['quantity'])
            # очистка корзины
        self.cart.clear()
