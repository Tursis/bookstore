from django.db.models import Sum
from django.shortcuts import get_object_or_404
from store.models import Product
from .models import Cart
from .cart_in_session import CartInSession


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
            self.cart.quantity = quantity
            self.cart.save()

    def __len__(self):
        """
        Подсчет количества товара в корзине
        """
        quantity = Cart.objects.filter(user=self.user).aggregate(Sum('quantity'))
        return quantity['quantity__sum']

    def get_total_price(self):
        """
        Подсчет суммы товаров в корзине.
        """
        return sum((item.product.get_discounted_price() * item.quantity for item in
                    Cart.objects.filter(user=self.user)))

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        cart_item = Cart.objects.filter(user=self.user).filter(product=product)
        cart_item.delete()

    def cart_quantity_update(self, data):
        """
        Обновление количества товара
        """
        for product in data:
            if product != 'csrfmiddlewaretoken':
                if data[product] == '0':
                    CartInModel.remove(self, product)
                else:
                    cart_item = Cart.objects.filter(user=self.user).get(product=product)
                    cart_item.quantity = data[product]
                    cart_item.save()
