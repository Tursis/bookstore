import django_filters
from django import forms
from django.db import models
from .models import Product, Book, Magazine, Category, BookGenre, BookAuthor, Publisher


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)
    book__genre = django_filters.ModelMultipleChoiceFilter(queryset=BookGenre.objects.all(),
                                                           widget=forms.CheckboxSelectMultiple)
    book__author = django_filters.ModelMultipleChoiceFilter(queryset=BookAuthor.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple)
    book__publisher = django_filters.ModelMultipleChoiceFilter(queryset=Publisher.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple)



    price = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Product
        fields = [
            'category',
            'price',
        ]
