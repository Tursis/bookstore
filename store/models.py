from django.db import models
from django.urls import reverse


# Create your models here.
class Book(models.Model):
    name = models.TextField(max_length=100, help_text="Enter book name.")
    author = models.TextField(max_length=50, help_text="Enter author name.")
    pages = models.TextField(max_length=5, help_text="Enter number of pages")
    publisher = models.TextField(max_length=50, help_text="Enter publisher name")
    pub_year = models.IntegerField(max_length=4, help_text="Enter year of publication")
    hard_cover = models.ImageField(upload_to='static/images/')
    size = models.TextField(max_length=10, help_text="Enter size book")
    price = models.DecimalField(max_length=10, help_text="Enter price book", decimal_places=2)
    Discounts = models.DecimalField(max_length=10, help_text="Enter discounts", decimal_places=2)


class Magazine(models.Model):
    name = models.TextField(max_length=100, help_text="Enter name Magazine")
    pages = models.IntegerField(max_length=3, help_text="Enter count pages Magazine")
    publisher = models.TextField(max_length=50, help_text="Enter publisher name")
    pub_year = models.IntegerField(max_length=4, help_text="Enter year of publication")
    numb = models.IntegerField(max_length=4, help_text="Enter number Magazine")
    numb_in_year = models.IntegerField(max_length=4, help_text="Enter number Magazine")
    size = models.TextField(max_length=10, help_text="Enter size book")
    price = models.DecimalField(max_length=10, help_text="Enter price book", decimal_places=2)
    subs_price = models.DecimalField(max_length=10, help_text="Enter price book", decimal_places=2)
    Discounts = models.DecimalField(max_length=10, help_text="Enter discounts", decimal_places=2)