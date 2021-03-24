from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from store.models import Product
from .models import ViewStatistics


def counter(function_to_decorate):
    def decorator(self, request, slug, *args, **kwargs):
        try:
            product = Product.objects.get(slug=slug)
            view_statistics = ViewStatistics()
            if ViewStatistics.objects.filter(product=product):
                view_statistics = ViewStatistics.objects.get(product=product)
                view_statistics.quantity += 1
                view_statistics.save()
            else:
                view_statistics.product = product
                view_statistics.quantity = 1
                view_statistics.save()
            return function_to_decorate(self, request, slug, *args, **kwargs)
        except ObjectDoesNotExist:
            return render(request, '404.html')
    return decorator
