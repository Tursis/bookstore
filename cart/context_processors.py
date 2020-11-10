from .cart import CartManager
from .cart_in_model import CartInDataBase, CartInSession


def cart(request,):
    return {'cart_info': CartManager(request)}
