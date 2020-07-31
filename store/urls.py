from . import views
from django.conf.urls import include, url
from . import views
from django.urls import path

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.index, name='index'),
    path('store/books/', views.BooksListView.as_view(), name='books'),
    path('store/books/genre', views.BookGenresListView.as_view(), name='book_genres'),
    path('store/magazine/', views.MagazineListView.as_view(), name='magazine'),
    path('store/books/<slug:slug>', views.BooksDetailView.as_view(), name='book_detail'),
    path('store/magazine/<slug:slug>', views.MagazineDetailView.as_view(), name='magazine_detail')
]
