from .cart_in_model import CartInModel
from .cart_in_session import CartInSession


class CartManager:

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        if request.user.is_anonymous:
            self.cart = CartInSession(request)

        else:
            self.cart = CartInModel(request)

    def add(self, request, product_id, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """

        if request.user.is_anonymous:
            self.cart.add(product_id, quantity, update_quantity=False)

        else:
            self.cart.add(product_id, quantity)

    def __len__(self):
        return self.cart.__len__()

    def get_total_price(self):
        return self.cart.get_total_price()

    def remove(self, product):
        return self.cart.remove(product)


