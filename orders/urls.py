from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.OrdersListView.as_view(), name='orders_list'),
    path('create/', views.OrderView.as_view(), name='order_view'),
]
