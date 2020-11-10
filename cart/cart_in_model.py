from store.models import Product
from django.db.models import Sum, Count, Avg
from .models import Cart


class CartInModel:
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
        cart_item = Cart.objects.filter(user=self.user).filter(product=product)
        cart_item.delete()

