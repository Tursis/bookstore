from django.db import models
from django.contrib.auth.models import User
from store.models import Product, Book, Magazine
from cart.models import Cart


# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True)
    email = models.EmailField(verbose_name='Електронная почта', null=True)
    address = models.CharField(max_length=250, verbose_name='Адрес', null=True)
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый код', null=True)
    city = models.CharField(max_length=100, verbose_name='Город', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='Проплата', null=True)

    def __str__(self):
        return '{}'.format(self.id)


class Purchase(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', null=True)
    price = models.DecimalField(max_digits=10, verbose_name='Цена', decimal_places=2, help_text="Enter price book",
                                blank=True)
    quantity = models.IntegerField(verbose_name='Количество', help_text="Количество товара", blank=True, default=0,
                                   null=True)
    purchase_date = models.DateTimeField('Дата покупки', auto_now=True)

    def __str__(self):
        return self.order
