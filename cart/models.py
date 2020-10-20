from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Cart(models.Model):
    """Модель корзины"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', null=True)
    quantity = models.IntegerField(verbose_name='Количество', help_text="Enter year of publication", blank=True,
                                   null=True)
