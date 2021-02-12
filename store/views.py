from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from bookstore.settings import PERMISSION_ON_SITE
from .forms import BookForm
from .models import Product, Book, Magazine, BookGenre
from comments.models import ProductReviews
from comments.comments import quantity_reviews, add_review_comment
from comments.forms import ReviewCommentForm
from comments.views import ReviewCommentView


# Create your views here.

class ProductListView(generic.ListView):
    template_name = 'index.html'
    model = Product
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context


def product_manage(request):
    return render(request, 'store/product_manage.html')


class BookGenresListView(generic.ListView):
    template_name = 'store/book/book_genres.html'
    model = BookGenre


class BooksListView(generic.ListView):
    model = Book
    paginate_by = 4
    template_name = 'store/book/book_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BooksDetailView(generic.DetailView):
    model = Book
    template_name = 'store/book/book_detail.html'

    def post(self, request, slug, **kwargs):
        ReviewCommentView.post(self, request, slug)
        return redirect('store:book_detail', slug=slug)

    def get_context_data(self, **kwargs):
        context = super(BooksDetailView, self).get_context_data(**kwargs)
        context['is_shown_by_default'] = True
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


class MagazineListView(generic.ListView):
    model = Magazine
    paginate_by = 4
    template_name = 'store/magazine/magazine_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MagazineDetailView(generic.DetailView):
    template_name = 'store/magazine/magazine_detail.html'
    model = Magazine

    def post(self, request, slug, **kwargs):
        ReviewCommentView.post(self, request, slug)
        return redirect('store:magazine_detail', slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_shown_by_default'] = True
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
