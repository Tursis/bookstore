from django.conf.urls import url
from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'profile'
urlpatterns = [
    path('profile', views.SignUpView.as_view(), name='sign_up'),
    path('profile/detail', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('activate/<token>', views.ActivateAccountView.as_view(), name='activate_account'),
]