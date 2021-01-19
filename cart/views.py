from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from store.models import Product
from .cart import CartManager, cart_quantity_update
from .cart_in_session import CartInSession
from .models import Cart
from .forms import CartAddProductForm
from .serializers import CartSerializer


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
    return render(request, 'cart/cart.html', {'cart': cart})


class CartUpdate(APIView):

    def post(self, request, format=None):
        cart_manager = CartManager(request)
        # data = JSONParser().parse(request)
        # print(data)
        # serializer = CartSerializer(request.data)
        cart_quantity_update(request.data)
        json = JSONRenderer().render([cart_manager.get_total_price(), cart_manager.__len__()])
        return Response(json)
