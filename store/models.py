from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class BookAuthor(models.Model):
    name = models.CharField(max_length=50, help_text="Enter author name.", blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name + ';'


class BookGenre(models.Model):
    genre = models.CharField(max_length=50,  help_text="Enter book genre.", blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return reverse('store:book_genres', kwargs={'slug': self.slug})


class Book(models.Model):
    name = models.CharField(max_length=100, help_text="Enter book name.", blank=True)
    author = models.ManyToManyField(BookAuthor)
    pages = models.CharField(max_length=5, help_text="Enter number of pages", blank=True)
    publisher = models.CharField(max_length=50, help_text="Enter publisher name", blank=True)
    pub_year = models.IntegerField(help_text="Enter year of publication", blank=True, null=True)
    hard_cover = models.CharField(max_length=1, help_text="Enter hard cover book (+/-)", blank=True)
    genre = models.ManyToManyField(BookGenre)
    size = models.CharField(max_length=10, help_text="Enter size book", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter price book", blank=True)
    Discounts = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter discounts", blank=True)
    image = models.ImageField(upload_to='images/books/', blank=True, null=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:book_detail', kwargs={'slug': self.slug})


class Magazine(models.Model):
    name = models.CharField(max_length=100, help_text="Enter name Magazine", blank=True)
    pages = models.IntegerField(help_text="Enter count pages Magazine", blank=True, null=True)
    publisher = models.CharField(max_length=50, help_text="Enter publisher name", blank=True)
    pub_year = models.IntegerField(help_text="Enter year of publication", blank=True, null=True)
    numb = models.IntegerField(help_text="Enter number Magazine", blank=True, null=True)
    numb_in_year = models.IntegerField(help_text="Enter number Magazine", blank=True, null=True)
    size = models.CharField(max_length=10, help_text="Enter size book", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter price book", blank=True, null=True)
    subs_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter price book", blank=True,
                                     null=True)
    Discounts = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter discounts", blank=True, null=True)
    image = models.ImageField(upload_to='images/magazine', blank=True, null=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:magazine_detail', kwargs={'slug': self.slug})
