from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from store.models import Product
from .models import Cart


class CartInDataBase:
    def __init__(self):
        self.cart = Cart()

    def add(self, user, product, quantity=1):
        product = product

        if Cart.objects.filter(user=user).filter(product=product):
            self.cart = Cart.objects.get(user=user, product=product)
            self.cart.quantity += quantity
            self.cart.save()
        else:
            self.cart.user = user
            self.cart.product = product
            self.cart.price = product.price
            self.cart.quantity = quantity
            self.cart.save()
