from .cart import CartManager
from .cart_save import CartInDataBase, CartInSession


def cart(request,):
    return {'cart': CartManager(request)}
