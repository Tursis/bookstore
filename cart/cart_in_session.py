from store.models import Product
from decimal import Decimal
from django.conf import settings


class CartInSession:

    def __init__(self, request):
        """
        Инициализация корзины в сесии
        """
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, update_quantity=False):
        """
        Добавление товара в корзину
        """
        if str(product_id) not in self.cart:
            self.cart[product_id] = {'quantity': quantity,
                                     }
        elif str(product_id) in self.cart:
            self.cart[str(product_id)]['quantity'] += 1
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
        Подсчет количества товара в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        """
        Подсчет суммы товаров в корзине.
        """
        for product in products:
            self.cart[str(product.id)]['price'] = str(product.get_discounted_price())
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        """
         удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def cart_quantity_update(self, data):
        for product in data:
            if product != 'csrfmiddlewaretoken':
                if product in self.cart:
                    self.cart[product]['quantity'] = int(data[product])
                    self.save()
