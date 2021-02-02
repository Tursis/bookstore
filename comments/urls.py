from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('add/<slug>', views.ProductReviewsView.as_view(), name='product_reviews'),

]
