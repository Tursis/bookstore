from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from store.models import Product
from .cart import CartManager
from .cart_in_session import CartInSession
from .models import Cart
from .forms import CartAddProductForm


class CartAddView(View):

    def post(self, request, product_id):
        cart = CartManager(request)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(request, product_id=product_id,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = CartManager(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
    else:
        cart = CartInSession(request)
    return render(request, 'cart/detail.html', {'cart': cart})
