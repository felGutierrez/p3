
## PARA MULTIPLICAR LA CANTIDAD DE UNIDADES POR EL VALOR EN CARRITO
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
 