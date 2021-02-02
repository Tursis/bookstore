from django.shortcuts import get_object_or_404
from store.models import Product
from .models import ProductComment
from .forms import ProductReviewsForm


def product_reviews(request, slug, form):
    product = get_object_or_404(Product, slug=slug)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.product = product
        new_comment.user = request.user
        new_comment.save()





