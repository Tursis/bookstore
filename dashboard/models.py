from django.db import models
from store.models import Product


# Create your models here.

class ViewStatistics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', null=True)
    quantity = models.IntegerField(verbose_name='Количество просмотров', blank=True, null=True)
