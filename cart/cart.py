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

        if request.user.is_authenticated:
            self.cart = CartInDataBase()

    def add(self, request, product_id, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product = Product.objects.get(id=product_id)
        if request.user.is_anonymous:
            self.cart.add(product, quantity, update_quantity=False)

        if request.user.is_authenticated:
            self.cart.add(request.user, product, quantity)

    def __len__(self):
        return self.cart.__len__()