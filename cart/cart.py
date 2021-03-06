from django.shortcuts import get_object_or_404

from .cart_in_model import CartInModel
from .cart_in_session import CartInSession
from .models import Cart
from store.models import Product


class CartManager:

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        if request.user.is_anonymous:
            self.cart = CartInSession(request)

        else:
            self.cart = CartInModel(request)

    def add(self, request, product_id, quantity=1):

        """
        Добавить продукт в корзину или обновить его количество.
        """

        if request.user.is_anonymous:
            self.cart.add(product_id, quantity)

        else:
            self.cart.add(product_id, quantity)

    def __len__(self):
        """
        Подсчет количества товара в корзине
        """
        return self.cart.__len__()

    def get_total_price(self):
        """
        Подсчет суммы товаров в корзине.
        """
        return self.cart.get_total_price()

    def remove(self, product):
        """
        Удаление товара из корзины
        """
        self.cart.remove(product)

    def cart_quantity_update(self, data):
        """
        Обновление количества товара в корзине
        """
        return self.cart.cart_quantity_update(data)
