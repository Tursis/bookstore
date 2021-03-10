from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from bookstore.settings import PERMISSION_ON_SITE
from .filter_counter import test
from .filters import ProductFilter
from .forms import BookForm
from .models import Product, Book, Magazine, BookGenre, BookAuthor, Category, Publisher
from comments.models import ProductReviews
from comments.comments import quantity_reviews
from comments.forms import ReviewCommentForm
from comments.views import ReviewCommentView

# Create your views here.
from .serializers import ProductSerializer


# class JsonFilterMoviesView(ListView):
#     """Фильтр фильмов в json"""
#
#     def get_queryset(self):
#         queryset = Product.objects.filter(
#             Q(category__in=self.request.GET.getlist("category"))
#         ).distinct().values("name", "price")
#
#         return queryset
#
#     def get(self, request, *args, **kwargs):
#         print('hello3')
#         queryset = list(self.get_queryset())
#         print(queryset)
#         print(request.GET)
#         return JsonResponse({"filter": queryset}, safe=False)
#
#     def get_context_data(self, *args, **kwargs):
#         print('context')
#         context = super().get_context_data(*args, **kwargs)
#         context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
#         return context

class ProductFilterView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'book__author']


class ProductListView(ListAPIView):
    def get(self, request):
        f = ProductFilter(request.GET, queryset=Product.objects.all())
        url_list = dict(request.GET)
        filter_counter(url_list, f, request)
        return render(request, 'index.html',
                      context={'filter': f, 'category_list': Category.objects.all(),
                               'author_list': BookAuthor.objects.all(), 'genre_list': BookGenre.objects.all(),
                               'publisher_list': Publisher.objects.all(), 'url_list': url_list})


def filter_counter(url_list, f, request):
    # print(url_list)
    # print(f.qs)
    print('Тест')
    # print(Product.objects.filter(category=1).filter(book__author=1))
    queryset = Product.objects.all()

    for item in request.GET:
        print(request.GET.getlist(item))
        print(item)
        if item == 'category':
            queryset = queryset.filter(Q(category__in=request.GET.getlist('category'))).distinct()
        if item == 'book__author':
            queryset = queryset.filter(Q(book__author__in=request.GET.getlist('book__author'))).distinct()
        if item == 'book__genre':
            queryset = queryset.filter(Q(book__genre__in=request.GET.getlist('book__genre'))).distinct()
        print(queryset.count())


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
