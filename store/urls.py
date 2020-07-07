from . import views
from django.conf.urls import include, url
from . import views
from django.urls import path

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.index, name='index'),
    path('store/books/', views.BooksListView.as_view(), name='books'),
    path('store/magazine/', views.MagazineListView.as_view(), name='magazine'),
    path('store/<slug:slug>', views.product_detail, name='product_detail'),
    path('store/<slug:slug>', views.MagazineDetailView.as_view(), name='product_detail')
]
