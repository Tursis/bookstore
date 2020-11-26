from .order_from_models import OrderFromModels
from .order_from_session import OrderFromSession
from django.shortcuts import render


class OrdersCreate:
    def __init__(self, request):
        if request.user.is_anonymous:
            self.order = OrderFromSession(request)

        else:
            self.order = OrderFromModels(request)

    def add_to_order(self, request, order):
        self.order.add_to_order(request, order)
