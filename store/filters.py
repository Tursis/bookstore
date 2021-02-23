from itertools import count

import django_filters
from django import forms
from django.db import models
from django.forms import ModelChoiceField

from .models import Product, Book, Magazine, Category, BookGenre, BookAuthor, Publisher


class CategoryMultipleChoceFilter(django_filters.ModelMultipleChoiceFilter):

    def filter(self, qs, value):
        print(qs)
        print(value)
        return super().filter(qs, {1: 'Журналы'})



class TestWidget(forms.CheckboxSelectMultiple):
    def get_context(self, name, value, attrs):
        return super().get_context(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        print(data, files, name)
        return super().value_from_datadict(data, files, name)



class ProductFilter(django_filters.FilterSet):
    # category = django_filters.ModelMultipleChoiceFilter(required=False,
    #                                         queryset=Category.objects.all(),
    #                                         widget=TestWidget,
    #                                         label="Non-compliant Assets"
    #                                         )
    category = CategoryMultipleChoceFilter(queryset=Category.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,

                                           )

    # category = RectificationAssetMultiField(required=False,
    #                                         queryset=Category.objects.all(),
    #                                         widget=forms.CheckboxSelectMultiple,
    #                                         label="Non-compliant Assets"
    #                                         )
    # book__genre = django_filters.ModelMultipleChoiceFilter(field_name='book__genre', queryset=BookGenre.objects.all(),
    #                                                        widget=forms.CheckboxSelectMultiple)
    #
    # book__author = django_filters.ModelMultipleChoiceFilter(field_name='book__author',
    #                                                         queryset=BookAuthor.objects.all(),
    #                                                         widget=forms.CheckboxSelectMultiple)
    # book__publisher = django_filters.ModelMultipleChoiceFilter(field_name='book__publisher',
    #                                                            queryset=Publisher.objects.all(),
    #                                                            widget=forms.CheckboxSelectMultiple)
    # print(book__publisher.queryset)
    # price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    # price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('kwarg_I_want_to_pass', None)
    #     super(ProductFilter, self).__init__(*args, **kwargs)
    #     print('hello')
    #     self.filters['category'].extra.update({
    #         'queryset': Category.objects.all(),
    #         'empty_label': '',
    #         'help_text': False,
    #
    #
    #     },
    #         widget=forms.CheckboxSelectMultiple(attrs={'class': 'test'}),
    #
    #     )

    class Meta:
        model = Product
        fields = [
            'category'
        ]
        # fields = [
        #
        #     'book__genre',
        #     'book__author',
        #     'book__publisher',
        #     'price',
        # ]

    def len(self):
        print(self.qs.values_list('category'))
        print(Category.objects.all())
        return Product.objects.values('name').count()
        # return count(self.qs)
