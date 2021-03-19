import operator

from django.db.models import Sum

from store.models import Product, Publisher, Category, BookGenre, BookAuthor
from orders.models import Purchase


def get_quantity_of_product_sold():
    quantity_of_product_sold_dict = {}
    sorted_dict = {}
    for purchase_product in Product.objects.all():
        quantity = Purchase.objects.filter(product=purchase_product).aggregate(Sum('quantity'))
        if quantity['quantity__sum'] is not None:
            quantity_of_product_sold_dict[purchase_product] = quantity['quantity__sum']
        else:
            quantity_of_product_sold_dict[purchase_product] = 0
    sorted_keys = sorted(quantity_of_product_sold_dict, key=quantity_of_product_sold_dict.get,
                         reverse=True)
    for product in sorted_keys:
        sorted_dict[product] = quantity_of_product_sold_dict[product]
    return sorted_dict
