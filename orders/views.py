from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View
from cart.models import Cart
from .models import Order, Purchase
from .forms import OrderCreateForm
from .orders import OrdersCreate


# Create your views here.
class OrderView(View):
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
        return render(request, 'orders/detail.html', {'form': form})
