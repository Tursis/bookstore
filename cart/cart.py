from decimal import Decimal
from django.conf import settings
from store.models import Product
from .cart_save import CartInDataBase, CartInSession


class CartManager:

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        if request.user.is_anonymous:
            self.cart = CartInSession(request)

        else:
            self.cart = CartInDataBase(request)

    def add(self, request, product_id, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """

        if request.user.is_anonymous:
            self.cart.add(product_id, quantity, update_quantity=False)

        else:
            self.cart.add(request.user, product_id, quantity)

    def __len__(self):
        return self.cart.__len__()