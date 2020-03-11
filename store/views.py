from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Book, Magazine

# Create your views here.

def index(request):
    return render(request, 'index.html')

class BooksListView(generic.ListView):
    model = Book
