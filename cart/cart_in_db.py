from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from store.models import Product
from .models import Cart


class CartInDataBase:
    def __init__(self):
        self.cart = Cart()

    def add(self, request, product_id, quantity=1, update_quantity=False):
        product = get_object_or_404(Product, id=product_id)
        if Cart.objects.filter(user=request.user).filter(product=product):
            self.cart = Cart.objects.get(user=request.user, product=product)
            self.cart.quantity += quantity
            self.cart.save()
        else:
            self.cart.user = request.user
            self.cart.product = product
            self.cart.price = product.price
            self.cart.quantity = quantity
            self.cart.save()
