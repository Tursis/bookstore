from django.shortcuts import render
from django.views.generic import View
from cart.models import Cart
from .models import Order, Purchase
from .forms import OrderCreateForm
from .orders import OrdersCreate


# Create your views here.
class OrderView(View):
    def post(self, request):
        order_create = OrdersCreate(request)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            order_create.add_to_order(request, order_form=form)
        else:
            form = OrderCreateForm
        return render(request, 'orders/detail.html', {'form': form})
