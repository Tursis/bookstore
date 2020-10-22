from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Cart(models.Model):
    """Модель корзины"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', null=True)
    quantity = models.IntegerField(verbose_name='Количество', help_text="Количество товара", blank=True, default=0,
                                   null=True)
    price = models.DecimalField(max_digits=10, verbose_name='Цена', decimal_places=2, help_text="Цена товара",
                                default=0,
                                blank=True)


