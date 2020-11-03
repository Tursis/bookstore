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

    def add(self, product, quantity=1, update_quantity=False):
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
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
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())


class CartInDataBase:
    def __init__(self):
        self.cart = Cart()

    def add(self, user, product, quantity=1, update_quantity=False):
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

    def __len__(self):
        queryset = Cart.objects.aggregate(Sum('quantity'))
        return queryset['quantity__sum']
