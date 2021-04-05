import django_filters
import transliterate
from django import forms

from .models import Product, Book, Magazine, Category, BookGenre, BookAuthor, Publisher




class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(required=False, queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)

    book__genre = django_filters.ModelMultipleChoiceFilter(required=False, field_name='book__genre',
                                                           queryset=BookGenre.objects.all(),
                                                           widget=forms.CheckboxSelectMultiple)

    book__author = django_filters.ModelMultipleChoiceFilter(required=False, field_name='book__author',
                                                            queryset=BookAuthor.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple)
    publisher = django_filters.ModelMultipleChoiceFilter(required=False,
                                                         queryset=Publisher.objects.all(),
                                                         widget=forms.CheckboxSelectMultiple)
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = [
            'category',
            'book__genre',
            'book__author',
            'publisher',
            'price',
        ]


class SearchFilter:
    def __init__(self, data):
        self.data = data

    def qs(self):

        request_data = transliterate.translit(self.data['q'], reversed=True)
        return Product.objects.filter(slug__icontains=request_data)



