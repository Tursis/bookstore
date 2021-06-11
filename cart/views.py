from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
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
            cart.add(request, product_id=product_id,
                     quantity=1, )
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
    return render(request, 'cart/cart.html', {'cart': cart})


class CartUpdate(APIView):
    """
    Клас обновление корзины(количества товара, сумы)
    """
    def post(self, request, format=None):
        cart_manager = CartManager(request)
        cart_manager.cart_quantity_update(request.data)
        json = JSONRenderer().render([cart_manager.get_total_price(), cart_manager.__len__()])
        return Response(json)
