from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, Purchase
from .forms import OrderCreateForm
from .orders import OrdersCreate, get_total_price


# Create your views here.
class OrderView(View):
    """
    Отображение формы заказа
    """
    def post(self, request):
        order_create = OrdersCreate(request)
        user = User.objects.get(username=request.user)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save()
                order_create.add_to_order(request, order)
                return render(request, 'orders/created.html', {'order': order})
        if request.user.is_authenticated:
            form = OrderCreateForm(initial={'first_name': user.first_name,
                                            'last_name': user.last_name,
                                            'email': user.email})
        else:
            form = OrderCreateForm
        return render(request, 'orders/create.html', {'form': form})


class OrdersListView(LoginRequiredMixin, View):
    """
    Отображение списка заказов
    """

    def get(self, request):
        user = User.objects.get(username=request.user)
        if request.user.is_authenticated:
            order = Order.objects.filter(email=user.email)

            return render(request, 'orders/orders_list.html', {'orders_list': order})


class OrdersDetailView(LoginRequiredMixin, View):
    """
    Отображение страницы заказов
    """

    def get(self, request, order_id):
        user = User.objects.get(username=request.user)
        order = Order.objects.get(id=order_id)
        if request.user.is_authenticated:
            if user.email == order.email:
                purchase = Purchase.objects.filter(order=order_id)
                total_price = get_total_price(purchase)
                return render(request, 'orders/orders_detail.html',
                              context={'order_id': order_id, 'purchase': purchase, 'total_price': total_price})
            else:
                return redirect('order:orders_list')
