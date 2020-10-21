from .cart import CartInSession
from .cart_in_db import CartInDataBase


def cart(request):
    return {'cart': CartInDataBase(request)}
