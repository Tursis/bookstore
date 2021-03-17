from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'dashboard'
urlpatterns = [path('statistics/', views.StatisticsView.as_view(), name='store_statistics'),
               ]

