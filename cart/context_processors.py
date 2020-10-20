from .cart import CartInSession


def cart(request):
    return {'cart': CartInSession(request)}
