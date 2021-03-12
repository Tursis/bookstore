from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.generics import ListAPIView

from bookstore.settings import PERMISSION_ON_SITE
from .filter_counter import product_filter_counter, update_model_counter
from .filters import ProductFilter
from .forms import BookForm
from .models import Product, Book, Magazine, BookGenre, BookAuthor, Category, Publisher
from comments.models import ProductReviews
from comments.comments import quantity_reviews
from comments.forms import ReviewCommentForm
from comments.views import ReviewCommentView


class ProductListView(ListAPIView):

    def get(self, request):
        f = ProductFilter(request.GET, queryset=Product.objects.all())
        url_list = dict(request.GET)
        product_filter_counter(request)
        return render(request, 'index.html',
                      context={'filter': f,
                               'category_list': update_model_counter(request, Category.objects.all()),
                               'author_list': update_model_counter(request, BookAuthor.objects.all()),
                               'genre_list': update_model_counter(request, BookGenre.objects.all()),
                               'publisher_list': update_model_counter(request, Publisher.objects.all()),
                               'url_list': url_list})


def product_manage(request):
    return render(request, 'store/product_manage.html')


class BooksDetailView(generic.DetailView):
    model = Book
    template_name = 'store/book/book_detail.html'

    def post(self, request, slug, **kwargs):
        ReviewCommentView.post(self, request, slug)
        return redirect('store:book_detail', slug=slug)

    def get_context_data(self, **kwargs):
        context = super(BooksDetailView, self).get_context_data(**kwargs)
        context['quantity_reviews'] = quantity_reviews(self.kwargs['slug'])
        context['reviews_list'] = ProductReviews.objects.filter(product__slug=self.kwargs['slug'])
        context['comment_form'] = ReviewCommentForm
        return context


class BooksManageView(PermissionRequiredMixin, generic.ListView):
    permission_required = PERMISSION_ON_SITE['moderator']
    model = Book
    template_name = 'store/book/book_manage.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BooksManageView, self).get_context_data(**kwargs)
        context['is_shown_by_default'] = True
        return context


class BooksCreate(PermissionRequiredMixin, CreateView):
    permission_required = PERMISSION_ON_SITE['moderator']
    model = Book
    form = BookForm
    fields = '__all__'
    template_name = 'store/book/book_create.html'


class BooksUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = PERMISSION_ON_SITE['moderator']
    model = Book
    form = BookForm
    fields = '__all__'
    template_name = 'store/book/book_update.html'


class BooksDelete(PermissionRequiredMixin, DeleteView):
    permission_required = PERMISSION_ON_SITE['moderator']
    model = Book
    form = BookForm
    template_name = 'store/book/book_delete.html'

    def get_success_url(self):
        return reverse('store:book_manage')


class MagazineDetailView(generic.DetailView):
    template_name = 'store/magazine/magazine_detail.html'
    model = Magazine

    def post(self, request, slug, **kwargs):
        ReviewCommentView.post(self, request, slug)
        return redirect('store:magazine_detail', slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quantity_reviews'] = quantity_reviews(self.kwargs['slug'])
        context['reviews_list'] = ProductReviews.objects.filter(product__slug=self.kwargs['slug'])
        context['comment_form'] = ReviewCommentForm
        return context


class MagazineManageView(PermissionRequiredMixin, generic.ListView):
    permission_required = PERMISSION_ON_SITE['moderator']
    model = Magazine
    template_name = 'store/magazine/magazine_manage.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MagazineManageView, self).get_context_data(**kwargs)
        context['is_shown_by_default'] = True
        return context


class MagazineCreate(PermissionRequiredMixin, CreateView):
    permission_required = PERMISSION_ON_SITE['moderator']
    model = Magazine
    form = BookForm
    fields = '__all__'
    template_name = 'store/magazine/magazine_create.html'


class MagazineUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = PERMISSION_ON_SITE['moderator']
    model = Magazine
    form = BookForm
    fields = '__all__'
    template_name = 'store/magazine/magazine_update.html'


class MagazineDelete(PermissionRequiredMixin, DeleteView):
    permission_required = PERMISSION_ON_SITE['moderator']
    model = Book
    form = BookForm
    template_name = 'store/magazine/magazine_delete.html'

    def get_success_url(self):
        return reverse('store:magazine_manage')
