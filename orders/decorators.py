from .utils import get_or_create_order
from carts.utils import get_or_create_cart

def validate_cart_and_order(function):
    def wrap(request, *args, **kwargs):
        cart_cart = get_or_create_cart(request)
        order = get_or_create_order(cart_cart, request)
        
        return function(request, cart_cart, order, *args, **kwargs)
    return wrap