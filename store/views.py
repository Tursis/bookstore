from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.utils import timezone
from .models import Book, Magazine, BookGenre, BookAuthor
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    book = Book.objects.all()
    magazine = Magazine.objects.all()
    genre = BookGenre.objects.all()
    product_list = sorted(
        chain(book, magazine),
        key=attrgetter('id'))
    paginator = Paginator(product_list, 6)
    page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)

    context = {'book': book, 'magazine': magazine, 'genre': genre, 'product_list': product_list}
    return render(request, 'index.html', context=context)


class ProductDetailView(generic.ListView):
    template_name = 'store/templates/product_detail.html'
    context_object_name = "product"

    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['magazine'] = Magazine.objects.all()
        context['product'] = sorted(chain(Book.objects.all(), Magazine.objects.all()), key=attrgetter('id'))
        context['is_shown_by_default'] = True
        return context


class BookGenresListView(generic.ListView):
    template_name = 'store/book_genres.html'
    model = BookGenre


class BooksListView(generic.ListView):
    model = Book
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Book.objects.all()
        return context


class MagazineListView(generic.ListView):
    model = Magazine
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Magazine.objects.all()
        return context


class BooksDetailView(generic.DetailView):
    template_name = 'store/book_detail.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BooksDetailView, self).get_context_data(**kwargs)
        context['product_list'] = get_object_or_404(Book,  slug=self.kwargs['slug'])
        context['is_shown_by_default'] = True
        return context


class MagazineDetailView(generic.DetailView):
    template_name = 'store/magazine_detail.html'
    model = Magazine

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = get_object_or_404(Magazine, slug=self.kwargs['slug'])
        context['is_shown_by_default'] = True
        return context
