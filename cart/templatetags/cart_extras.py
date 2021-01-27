from django import template

register = template.Library()


@register.filter
def mul(value, mul):
    """
    Тег для подсчета суми товара
    """
    return value * mul
