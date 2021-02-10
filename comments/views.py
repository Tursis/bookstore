from django.shortcuts import render, redirect
from django.views import View
from .comments import add_product_reviews, add_review_comment
from .forms import ProductReviewsForm, ReviewCommentForm


class ProductReviewsView(View):
    """
    Отображение формы заполнения отзыва
    """
    def post(self, request, slug, **kwargs):
        if request.method == 'POST':
            form = ProductReviewsForm(request.POST)
            if form.is_valid():
                form_reviews = form.save()
                add_product_reviews(request, slug, form)
                return redirect('store:book_detail', slug=slug)

            else:
                form_reviews = ProductReviewsForm
            return render(request, 'product_reviews.html', {'form_reviews': form_reviews, 'slug': slug})


class ReviewCommentView(View):
    def post(self, request, slug, **kwargs):
        if request.method == 'POST':
            form = ReviewCommentForm(request.POST)
            if form.is_valid():
                add_review_comment(request, slug, form)


