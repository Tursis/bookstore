from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('store/add/(?P<product_id>\d+)/', views.cart_add, name='cart_add'),
    path('store/remove/(?P<product_id>\d+)/', views.cart_remove, name='cart_remove'),
]