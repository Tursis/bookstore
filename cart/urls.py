from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [path('', views.cart_detail, name='cart_detail'),
               path('store/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
               ]
