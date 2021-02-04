from django.db.models import Sum
from django.shortcuts import get_object_or_404
from store.models import Product
from .models import ProductComment
from .forms import ProductReviewsForm


def product_reviews(request, slug, form):
    """
    Функция добавление отзыва товара
    """
    product = get_object_or_404(Product, slug=slug)
    if form.is_valid():
        new_reviews = form.save(commit=False)
        new_reviews.product = product
        new_reviews.user = request.user
        new_reviews.save()


def quantity_reviews(slug):
    """
    Подсчет количества отзывов товара
    """
    product = Product.objects.get(slug=slug)
    products_reviews = ProductComment.objects.filter(product=product).aggregate(Sum('product'))
    if products_reviews['product__sum']:
        return products_reviews['product__sum']
    else:
        return 0


def get_average_rating(slug):
    return slug
