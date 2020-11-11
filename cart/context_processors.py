from .cart import CartManager


def cart(request):
    return {'cart_info': CartManager(request)}
