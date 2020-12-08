from django.shortcuts import render
from cart.cart_in_session import CartInSession
from cart.models import Cart
from .models import Purchase, Product
from .forms import OrderCreateForm


class OrderFromModels:
    def __init__(self, request):
        self.cart = Cart.objects.filter(user=request.user)

    def add_to_order(self, request, order):
        for item_cart in self.cart:
            product = Product.objects.get(name=item_cart.product)
            Purchase.objects.create(order=order,
                                    product=item_cart.product,
                                    price=product.price,
                                    quantity=item_cart.quantity)
            # очистка корзины
            item_cart.delete()


