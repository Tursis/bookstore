from django.db import models
from django.urls import reverse


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100, help_text="Enter book name.")
    author = models.CharField(max_length=50, help_text="Enter author name.")
    pages = models.CharField(max_length=5, help_text="Enter number of pages")
    publisher = models.CharField(max_length=50, help_text="Enter publisher name")
    pub_year = models.IntegerField(help_text="Enter year of publication")
    hard_cover = models.ImageField(upload_to='static/images/')
    size = models.CharField(max_length=10, help_text="Enter size book")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter price book")
    Discounts = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter discounts")


class Magazine(models.Model):
    name = models.CharField(max_length=100, help_text="Enter name Magazine")
    pages = models.IntegerField(help_text="Enter count pages Magazine")
    publisher = models.CharField(max_length=50, help_text="Enter publisher name")
    pub_year = models.IntegerField(help_text="Enter year of publication")
    numb = models.IntegerField(help_text="Enter number Magazine")
    numb_in_year = models.IntegerField(help_text="Enter number Magazine")
    size = models.CharField(max_length=10, help_text="Enter size book")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter price book")
    subs_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter price book")
    Discounts = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter discounts")