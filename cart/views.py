import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from .cart import CartManager
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
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        cart = Cart.objects.all()
        print('test')
        serializer = CartSerializer(cart, many=True)
        cart = Cart.objects.get(pk='116')
        cart.quantity = (cart.quantity + 1)

        cart.save()
        return Response(serializer.data)

        # data = serializer.data['product']
        # print(data)
        # CartItem = Cart.objects.get(product=data)
        # CartItem.quantity = (CartItem.quantity + 1)
        # CartItem.save()

    def post(self, request, format=None):
        cartM = CartManager(request)
        cart = Cart.objects.all()
        print('test')
        serializer = CartSerializer(cart, many=True)
        cart = Cart.objects.get(pk='116')
        cart.quantity = (cart.quantity + 1)
        cart.save()
        cartM.get_total_price()
        return Response('test')