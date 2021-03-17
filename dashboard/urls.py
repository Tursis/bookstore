from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'dashboard'
urlpatterns = [path('', views.cart_detail, name='store_statistics'),
               ]

