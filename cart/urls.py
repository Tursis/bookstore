from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'cart'
urlpatterns = [path('', views.cart_detail, name='cart_detail'),
               path('store/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
               path('store/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
               path('testing_list/', views.testing_list, name="testing_list"),
               path('testing_api/<int:pk>/', views.testing_api, name="testing_api"),
               ]
urlpatterns = format_suffix_patterns(urlpatterns)
