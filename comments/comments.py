from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from store.models import Product
from .models import ProductReviews, ReviewComment
from .forms import ProductReviewsForm


def add_product_reviews(request, slug, form):
    """
    Функция добавление отзыва товара
    """
    product = get_object_or_404(Product, slug=slug)
    if form.is_valid():
        new_reviews = form.save(commit=False)
        new_reviews.product = product
        new_reviews.user = request.user
        new_reviews.save()


def add_review_comment(request, slug, form):
    product = get_object_or_404(Product, slug=slug)
    review_id = get_object_or_404(ProductReviews, id=request.POST.get('reviews'))
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.product = product
        new_comment.reviews = review_id
        new_comment.user = request.user
        new_comment.save()


def quantity_reviews(slug):
    """
    Подсчет количества отзывов товара
    """
    product = Product.objects.get(slug=slug)
    products_reviews = ProductReviews.objects.filter(product=product).aggregate(Count('product'))
    if products_reviews['product__count']:
        return products_reviews['product__count']
    else:
        return 0



