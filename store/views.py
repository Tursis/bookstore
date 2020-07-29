from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
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
    products = sorted(
        chain(book, magazine),
        key=attrgetter('id'))
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'book': book, 'magazine': magazine, 'genre': genre, 'products': products}
    return render(request, 'index.html', context=context)


def product_detail(request, slug):
    book = Book.objects.all()
    magazine = Magazine.objects.all()
    genre = BookGenre.objects.all()
    products = sorted(
        chain(book, magazine),
        key=attrgetter('id'))
    context = {'products': products, 'book': book, 'magazine': magazine, 'genre': genre, 'is_shown_by_default': True}
    return render(request, 'store/product_detail.html', context=context)


class BookGenresListView(generic.ListView):
    template_name = 'store/book_genres.html'
    model = BookGenre


class BooksListView(generic.ListView):
    model = Book
    paginate_by = 3


class MagazineListView(generic.ListView):
    model = Magazine
    paginate_by = 3


class BooksDetailView(generic.DetailView):
    template_name = 'store/product_detail.html'
    model = Book


class MagazineDetailView(generic.DetailView):
    template_name = 'store/product_detail.html'
    model = Magazine
