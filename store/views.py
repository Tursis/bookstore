from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .forms import BookForm, MagazineForm
from .models import Book, Magazine, BookGenre, BookAuthor
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from bookstore.settings import PERMISSION_ON_SITE


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


def product_manage(request):
    return render(request, 'store/product_manage.html')


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

    def get_context_data(self, **kwargs):
        context = super(BooksDetailView, self).get_context_data(**kwargs)
        context['is_shown_by_default'] = True
        context['cart_product_form'] = CartAddProductForm()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_shown_by_default'] = True
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
