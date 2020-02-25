from django.db import models
from django.urls import reverse

# Create your models here.
class Book(models.Model):
    name = models.TextField(max_length=100, help_text="Enter book name.")
    author = models.TextField(max_length=50, help_text="Enter author name.")
    pages = models.TextField(max_length=5, help_text="Enter number of pages")