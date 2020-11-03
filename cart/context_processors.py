from .cart import CartManager
from .cart_in_db import CartInDataBase


def cart(request):
    return {'cart': CartManager(request)}
