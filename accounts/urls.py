from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('store', views.SignUpView.as_view(), name='sign_up'),
]