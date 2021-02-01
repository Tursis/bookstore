from django.shortcuts import get_object_or_404
from store.models import Product
from .forms import ProductCommentForm


def product_comments(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        comment_form = ProductCommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.save()


