from cart.models import Cart
from .models import Purchase, Product


class OrderFromModels:
    """
    Перенос товаров из модели корзины в заказ.
    """
    def __init__(self, request):
        self.cart = Cart.objects.filter(user=request.user)

    def add_to_order(self, order):
        for item_cart in self.cart:
            product = Product.objects.get(name=item_cart.product)
            Purchase.objects.create(order=order,
                                    product=item_cart.product,
                                    price=product.get_discounted_price(),
                                    quantity=item_cart.quantity)
            # очистка корзины
            item_cart.delete()


