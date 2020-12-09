from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView
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
        return render(request, 'orders/create.html', {'form': form})


class OrdersListView(ListView):
    model = Order
    template_name = 'orders/orders_list.html'

    def get_context_data(self, **kwargs):
        context = super(OrdersListView, self).get_context_data(**kwargs)
        context['purchase'] = Purchase.objects.all()
        return context


class OrdersDetailView(DetailView):
    model = Purchase
