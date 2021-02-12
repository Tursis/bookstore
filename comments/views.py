from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .comments import add_product_reviews, add_review_comment
from .forms import ProductReviewsForm, ReviewCommentForm


class ProductReviewsView(LoginRequiredMixin, View):
    """
    Отображение формы заполнения отзыва
    """

    def post(self, request, slug, **kwargs):
        if request.method == 'POST':
            form = ProductReviewsForm(request.POST)
            if form.is_valid():
                add_product_reviews(request, slug, form)
                return HttpResponseRedirect(request.POST.get('next', '/'))
            else:
                form_reviews = ProductReviewsForm
            return render(request, 'product_reviews.html', {'form_reviews': form_reviews, 'slug': slug})


class ReviewCommentView(LoginRequiredMixin, View):

    def post(self, request, slug):
        if request.method == 'POST':
            form = ReviewCommentForm(request.POST)
            if form.is_valid():
                add_review_comment(request, slug, form)
