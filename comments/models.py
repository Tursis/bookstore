from django.db import models
from django.contrib.auth.models import User

from store.models import Product


class ProductReviews(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=400, verbose_name='Коментарий', help_text='Enter your comment here')
    rating = models.IntegerField(verbose_name='Оценка', help_text='Enter rating here',
                                 choices=RATING_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, verbose_name='активация коментария')

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title = 75
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + '...'
        else:
            titlestring = self.description
        return titlestring


class ReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reviews = models.ForeignKey(ProductReviews, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(max_length=400, verbose_name='Коментарий', help_text='Enter your comment here')
    pub_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, verbose_name='активация коментария')

    class Meta:
        ordering = ['pub_date']




