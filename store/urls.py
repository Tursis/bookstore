from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'store'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    url(r'^store$', views.ProductListView.as_view(), name='index', ),
    url(r'^search/$', views.SearchView.as_view(), name='search', ),
    path('store/manage/', views.ProductManage.as_view(), name='product_manage'),
    path('store/manage/book/', views.BooksManageView.as_view(), name='book_manage'),
    path('store/manage/magizne/', views.MagazineManageView.as_view(), name='magazine_manage'),
    path('store/books/<slug:slug>', views.BooksDetailView.as_view(), name='book_detail'),
    path('store/books/create/', views.BooksCreate.as_view(), name='book_create'),
    path('store/books/update/<slug:slug>', views.BooksUpdate.as_view(), name='book_update'),
    path('store/books/delete/<slug:slug>', views.BooksDelete.as_view(), name='book_delete'),
    path('store/magazine/<slug:slug>', views.MagazineDetailView.as_view(), name='magazine_detail'),
    path('store/magazine/create/', views.MagazineCreate.as_view(), name='magazine_create'),
    path('store/magazine/update/<slug:slug>', views.MagazineUpdate.as_view(), name='magazine_update'),
    path('store/magazine/delete/<slug:slug>', views.MagazineDelete.as_view(), name='magazine_delete'),
]
