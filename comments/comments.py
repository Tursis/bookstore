from django.shortcuts import get_object_or_404
from store.models import Product
from .models import ProductComment
from .forms import ProductReviewsForm


def product_reviews(request, slug, form):
    product = get_object_or_404(Product, slug=slug)
    if form.is_valid():
        new_reviews = form.save(commit=False)
        new_reviews.product = product
        new_reviews.user = request.user
        new_reviews.save()





