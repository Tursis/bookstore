import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
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
    return render(request, 'cart/cart.html', {'cart': cart})


def updateItem(request):
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
