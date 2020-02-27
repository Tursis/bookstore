from django.db import models
from store.models import Book, Magazine
# Create your models here.

class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    magazine = models.ForeignKey(Magazine, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField('order date')


class Purchase(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField('order date')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)