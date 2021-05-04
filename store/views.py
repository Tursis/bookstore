from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from bookstore.settings import PERMISSION_ON_SITE
from .filter_counter import product_filter_counter, update_model_counter
from .filters import ProductFilter, SearchFilter
from .forms import BookForm
from .models import Product, Book, Magazine, BookGenre, BookAuthor, Category, Publisher
from comments.models import ProductReviews
from comments.comments import quantity_reviews
from comments.forms import ReviewCommentForm
from comments.views import ReviewCommentView
from dashboard.decorator import counter


class ProductListView(View):

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


class ProductManage(PermissionRequiredMixin, View):
    permission_required = PERMISSION_ON_SITE['moderator']

    def get(self, request):
        return render(request, 'store/product_manage.html')


class BooksDetailView(View):
    @counter
    def get(self, requset, slug, **kwargs):
        book = Book.objects.get(slug=slug)
        return render(requset, 'store/book/book_detail.html', context={'book': book,
                                                                       'quantity_reviews': quantity_reviews(
                                                                           self.kwargs['slug']),
                                                                       'reviews_list': ProductReviews.objects.filter(
                                                                           product__slug=self.kwargs['slug']),
                                                                       'comment_form': ReviewCommentForm
                                                                       })

    def post(self, request, slug, **kwargs):
        ReviewCommentView.post(self, request, slug)
        return redirect('store:book_detail', slug=slug)


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


class MagazineDetailView(View):
    @counter
    def get(self, requset, slug, **kwargs):
        magazine = Magazine.objects.get(slug=slug)
        return render(requset, 'store/magazine/magazine_detail.html', context={'magazine': magazine,
                                                                               'quantity_reviews': quantity_reviews(
                                                                                   self.kwargs['slug']),
                                                                               'reviews_list': ProductReviews.objects.filter(
                                                                                   product__slug=self.kwargs['slug']),
                                                                               'comment_form': ReviewCommentForm
                                                                               })

    def post(self, request, slug, **kwargs):
        ReviewCommentView.post(self, request, slug)
        return redirect('store:magazine_detail', slug=slug)


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
    """
    Создание журналов
    """
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


class SearchView(View):
    def get(self, request):
        # f = search_filter(request.GET, queryset=Product.objects.all())
        f = SearchFilter(request.GET)
        return render(request, 'index.html',
                      context={'filter': f})


def handler404(request, exception):
    data = {}
    return render(request, '404.html', data)


def handler500(request):
    return render(request, '500.html')
