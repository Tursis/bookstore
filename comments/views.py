from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .comments import product_reviews
from .forms import ProductReviewsForm


class ProductReviewsView(View):

    def post(self, request, slug, **kwargs):
        if request.method == 'POST':
            form = ProductReviewsForm(request.POST)
            if form.is_valid():
                form_reviews = form.save()
                product_reviews(request, slug, form)
                return HttpResponseRedirect(request.POST.get('next', '/'))

            else:
                form_reviews = ProductReviewsForm
            return render(request, 'product_reviews.html', {'form_reviews': form_reviews, 'slug': slug})
