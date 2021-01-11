import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
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


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    CartItem = Cart.objects.get(product=product)

    if action == 'add':
        CartItem.quantity = (CartItem.quantity + 1)
    elif action == 'remove':
        CartItem.quantity = (CartItem.quantity - 1)

    CartItem.save()

    if CartItem.quantity <= 0:
        CartItem.delete()

    return JsonResponse('Item was added', safe=False)


@api_view(['GET', 'POST'])
def testing_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Cart.objects.all()
        serializer = CartSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def testing_api(request, pk, format=None):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CartSerializer(cart)
        data = serializer.data['product']
        print(data)
        CartItem = Cart.objects.get(product=data)
        CartItem.quantity = (CartItem.quantity + 1)
        CartItem.save()
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CartSerializer(cart, data=data)
        if serializer.is_valid():
            data = serializer.data['product']
            print(data)
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
