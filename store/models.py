from itertools import count

from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .filter_counter import test

# Create your models here.


class BookAuthor(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя', help_text="Enter author name.", blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name + ';'

    def len(self):
        return Book.objects.filter(author=self.id).count()


class BookGenre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Жанр', help_text="Enter book genre.", blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:book_genres', kwargs={'slug': self.slug})

    def len(self):

        return Book.objects.filter(genre=self.id).count()


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория товару', help_text="Enter product category.",
                            blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def len(self):
        return Product.objects.filter(category=self.id).count()


class Publisher(models.Model):
    name = models.CharField(max_length=50, verbose_name='Жанр', help_text="Enter publisher.", blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def len(self):
        return Book.objects.filter(publisher=self.id).count()


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name='Название', help_text="Enter book name.", blank=True)

    price = models.DecimalField(max_digits=10, verbose_name='Цена', decimal_places=2, help_text="Enter price book",
                                validators=[MinValueValidator(1)],
                                blank=True)
    Discounts = models.DecimalField(max_digits=10, verbose_name='Скидка', decimal_places=2, help_text="Enter discounts",
                                    validators=[MinValueValidator(0)],
                                    blank=True)
    image = models.ImageField(upload_to='images/books/', verbose_name='Изображение', blank=True, null=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        ссылка на товар
        """
        if self.category.name == 'Книги':
            return reverse('store:book_detail', kwargs={'slug': self.slug})
        else:
            return reverse('store:magazine_detail', kwargs={'slug': self.slug})

    def get_rating(self):
        """
        Получение рейтинга товара
        """
        rating = self.productreviews_set.all().aggregate(Avg('rating'))
        if rating['rating__avg']:
            return 'Рейтинг: %s' % (round(float(rating['rating__avg']), 2))
        else:
            return ''

    def get_discount(self):
        """
        Получение скидки больше
        """
        category_discount = self.category.categorydiscount_set.get(category=self.category)
        if category_discount.discount > self.Discounts:
            return category_discount.discount
        else:
            return self.Discounts

    def get_discounted_price(self):
        """
        Получение цены товара на основе скидки
        """
        discount = self.get_discount()
        if discount > 0:
            price = self.price - (self.price * (discount / 100))
            return price
        if discount == 0:
            return self.price


class Book(Product):
    author = models.ManyToManyField(BookAuthor, verbose_name='Автор')
    genre = models.ManyToManyField(BookGenre, verbose_name='Жанр')
    hard_cover = models.CharField(max_length=1, verbose_name='Твердая обложка', help_text="Enter hard cover book (+/-)",
                                  blank=True)
    pages = models.CharField(max_length=5, verbose_name='Количество страниц', help_text="Enter number of pages",
                             blank=True)
    pub_year = models.IntegerField(verbose_name='Год издания', help_text="Enter year of publication", blank=True,
                                   null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=10, verbose_name='Размеры', help_text="Enter size book", blank=True)


class Magazine(Product):
    numb = models.IntegerField(verbose_name='Номер журнала', help_text="Enter number Magazine", blank=True, null=True)
    numb_in_year = models.IntegerField(verbose_name='Номер журнала в году', help_text="Enter number Magazine",
                                       blank=True, null=True)
    subs_price = models.DecimalField(max_digits=10, verbose_name='Цена подписки', decimal_places=2,
                                     help_text="Enter price book", blank=True,
                                     null=True)
    pages = models.CharField(max_length=5, verbose_name='Количество страниц', help_text="Enter number of pages",
                             blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    pub_year = models.IntegerField(verbose_name='Год издания', help_text="Enter year of publication", blank=True,
                                   null=True)
    size = models.CharField(max_length=10, verbose_name='Размеры', help_text="Enter size book", blank=True)


class CategoryDiscount(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    discount = models.DecimalField(max_digits=10, verbose_name='Скидка', decimal_places=2, help_text="Enter discounts",
                                   validators=[MinValueValidator(0)],
                                   blank=True)
    active = models.BooleanField(default=False, verbose_name='активация скидки')

    def __str__(self):
        return self.discount
