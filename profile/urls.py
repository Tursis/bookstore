from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path('profile', views.SignUpView.as_view(), name='sign_up'),
]