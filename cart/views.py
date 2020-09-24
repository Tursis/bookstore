from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from store.models import Book, Magazine
from .cart import Cart
from .forms import CartAddProductForm


class CartAddView(CreateView):
    def __init__(self, product_id):
        self.product_id = product_id

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Book, id=self.product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data
            cart.add(product=product,
                     quantity=item['quantity'],
                     update_quantity=item['update'])
            cart.save()
        return render(request, 'cart/detail.html', context={'cart': cart})


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
