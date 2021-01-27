from django.shortcuts import get_object_or_404
from .models import Product
from .forms import ProductCommentForm


def product_comments(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = ProductCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = ProductCommentForm()
    return comment_form
