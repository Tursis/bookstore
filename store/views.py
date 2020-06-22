from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Book, Magazine
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    book = Book.objects.all()
    magazine = Magazine.objects.all()
    result_list = sorted(
        chain(book, magazine),
        key=attrgetter('id'))
    context = {'book': book, 'magazine': magazine, 'result_list': result_list}
    return render(request, 'index.html', context=context)



class BooksListView(generic.ListView):
    model = Book
    paginate_by = 3


class MagazineListView(generic.ListView):
    model = Magazine
    paginate_by = 3
