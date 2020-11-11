from django.db.models import Sum, Count, Avg
from store.models import Product
from .models import Cart
from .cart_in_session import CartInSession
from bookstore import settings


class CartInModel:
    """
    Клас сохранение корзины в модель
    """

    def __init__(self, request):
        """"
        Инициализация корзины, та заполнение модели корзины данными из сесии
        """
        self.cart = Cart()
        self.user = request.user
        self.cart_session = CartInSession(request)
        if self.cart_session.cart:
            for product in self.cart_session.cart:
                CartInModel.add(self, int(product), self.cart_session.cart[product]['quantity'])
            self.cart_session.clear()

    def add(self, product_id, quantity=1):
        """
        Додавания товара в корзину
        """
        product = Product.objects.get(id=product_id)
        if Cart.objects.filter(user=self.user).filter(product=product):
            self.cart = Cart.objects.get(user=self.user, product=product)
            self.cart.quantity += quantity
            self.cart.save()
        else:
            self.cart.user = self.user
            self.cart.product = product
            # self.cart.price = product.price
            self.cart.quantity = quantity
            self.cart.save()

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        quantity = Cart.objects.filter(user=self.user).aggregate(Sum('quantity'))
        return quantity['quantity__sum']

    def get_total_price(self):
        return sum((item.product.price * item.quantity for item in
                    Cart.objects.filter(user=self.user)))

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        cart_item = Cart.objects.filter(user=self.user).filter(product=product)
        cart_item.delete()

    def test(self):
        return self.cart_session.cart
