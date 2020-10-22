from django.contrib.auth.models import User
from store.models import Product
from .models import Cart


class CartInDataBase:
    def __init__(self):
        self.cart = Cart()

    def add(self, request, product, quantity=1, update_quantity=False):
        if Cart.objects.filter(user=request.user) and Cart.objects.filter(product=product):
            self.cart = Cart.objects.get(product=product)
            self.cart.quantity += quantity
            self.cart.save()
        else:
            self.cart.user = request.user
            self.cart.product = product
            self.cart.price = product.price
            self.cart.quantity = quantity
            self.cart.save()
