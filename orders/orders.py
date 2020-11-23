from .order_from_models import OrderFromModels
from .order_from_session import OrderFromSession


class OrdersCreate:
    def __init__(self, request):
        if request.user.is_anonymous:
            self.cart = OrderFromSession(request)

        else:
            self.cart = OrderFromModels(request)
