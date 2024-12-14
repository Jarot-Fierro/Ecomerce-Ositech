from .models import Order

from django.urls import reverse

def get_or_create_order(cart, request):
    order = cart.order
    
    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)
    
    if order:
        request.session['order_id'] = order.order_id
        
    return order


def breadcrumb(products=True, address=False, confirmation=False,  payment=False):
    return [
        {'title':'Productos', 'active':products, 'url':reverse('orders:order')},
        {'title':'Dirección', 'active':address, 'url':reverse('orders:address')},
        {'title':'Confirmación', 'active':confirmation, 'url':reverse('orders:confirm')},
        {'title':'Pago', 'active':payment, 'url':reverse('orders:order')},
        


    ]
    
def destroy_order(request):
    request.session['order_id'] = None
    