from django.shortcuts import render
from cart.cart_in_session import CartInSession
from .models import Purchase, Product
from .forms import OrderCreateForm


class OrderFromModels:
    def __init__(self, request):
        self.cart = CartInSession(request)
        self.purchase = Purchase()

    def add_to_order(self, request, order_form):
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in self.cart:
                Purchase.objects.create(order=order,
                                        product=item['product'],
                                        price=item['quantity'],
                                        quantity=item['quantity'])
            # очистка корзины
            self.cart.clear()
            return render(request, 'orders/created.html',
                          {'order': order})
