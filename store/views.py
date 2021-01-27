from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import PermissionRequiredMixin
from itertools import chain
from operator import attrgetter
from bookstore.settings import PERMISSION_ON_SITE
from .forms import BookForm, MagazineForm, ProductCommentForm
from .models import Book, Magazine, BookGenre
from cart.forms import CartAddProductForm
from .comments import product_comments


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

    def post(self, request, product_id):
        comment = product_comments(request, product_id)
        context = {'comment_form': 'hello'}
        return render('store/book/book_detail.html', context)

    def get_context_data(self, **kwargs):
        context = super(BooksDetailView, self).get_context_data(**kwargs)
        context['is_shown_by_default'] = True
        context['product_comment_form'] = ProductCommentForm()
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
        context['cart_product_form'] = CartAddProductForm()
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
