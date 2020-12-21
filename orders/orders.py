from django.contrib.auth.models import User
from .order_from_models import OrderFromModels
from .order_from_session import OrderFromSession
from .models import Purchase


class OrdersCreate:
    """
    Создание закака.
    """
    def __init__(self, request):
        self.user = User.objects.get(username=request.user)
        if request.user.is_anonymous:
            self.order = OrderFromSession(request)

        else:
            self.order = OrderFromModels(request)

    def add_to_order(self, request, order):
        self.order.add_to_order(request, order)


def get_total_price(purchase):
    """
    Подсчет суммы товаров в заказе.
    """
    return sum((item.product.price * item.quantity for item in
                purchase))
