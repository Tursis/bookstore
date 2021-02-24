from itertools import count

import django_filters
from django import forms
from django.db import models
from django.db.models import Q
from django.forms import ModelChoiceField

from .models import Product, Book, Magazine, Category, BookGenre, BookAuthor, Publisher


class CategoryMultipleChoceFilter(django_filters.ModelMultipleChoiceFilter):

    def filter(self, qs, value):
        return super().filter(qs, value)


class MyPropertyFilter(django_filters.Filter):
    def filter(self, qs, value):
        result = qs
        result.count = len(result)
        return result


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(required=False,
                                                        queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple(),
                                                        label="Non-compliant Assets"
                                                        )

    book__genre = django_filters.ModelMultipleChoiceFilter(field_name='book__genre', queryset=BookGenre.objects.all(),
                                                           widget=forms.CheckboxSelectMultiple)

    book__author = django_filters.ModelMultipleChoiceFilter(field_name='book__author',
                                                            queryset=BookAuthor.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple)
    book__publisher = django_filters.ModelMultipleChoiceFilter(field_name='book__publisher',
                                                               queryset=Publisher.objects.all(),
                                                               widget=forms.CheckboxSelectMultiple)
    print(book__publisher.queryset)
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = [
            'category',
            'book__genre',
            'book__author',
            'book__publisher',
            'price',
        ]

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)
        for item in self.form.fields['category'].queryset:
            print(item.len())
