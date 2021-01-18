from django import template

register = template.Library()


@register.filter
def mul(value, mul):
    return value * mul
