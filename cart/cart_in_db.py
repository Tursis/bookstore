from django.contrib.auth.models import User
from store.models import Product
from .models import Cart


class CartInDataBase:
    def __init__(self, request):
        self.cart = Cart()
        self.cart.user = request.user

    def add(self, product, quantity=1, update_quantity=False):
        self.cart.product = product
        self.cart.price = product.price
        self.cart.quantity = quantity
        self.cart.save()
