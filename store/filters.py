import django_filters

from .models import Product, Book, Magazine, Category
from django import forms


class ProductFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    name = django_filters.ModelMultipleChoiceFilter(queryset=Product.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple)

    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)



class Meta:
        model = Product
        fields = ['name', 'price', 'category']
