from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from store.models import Product
from decimal import Decimal
from django.db.models import Sum, Count, Avg
from django.conf import settings
from .models import Cart


class CartInSession:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, update_quantity=False):
        product = Product.objects.get(id=product_id)
        product_id = product_id
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):

        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['quantity']) * item['quantity'] for item in
                   self.cart.values())


class CartInDataBase:
    """
    Клас сохранение корзины в модель
    """

    def __init__(self, request):
        self.cart = Cart()
        self.user = request.user

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
        product = Cart.objects.get(product=product)
        product.delete()
