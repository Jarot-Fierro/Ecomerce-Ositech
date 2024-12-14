from django.shortcuts import render, redirect

from .models import Order
from carts.utils import get_or_create_cart
# Create your views here.

from shipping_addresses.models import ShippingAddress

from .utils import get_or_create_order

from django.contrib.auth.decorators import login_required

from .utils import breadcrumb

from django.shortcuts import get_object_or_404



from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView

from django.db.models.query import EmptyQuerySet

from .decorators import validate_cart_and_order

from django.urls import reverse


class OrderListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'orders/list_orders.html'
    
    def get_queryset(self):
        return self.request.user.orders_completed()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for order in context['object_list']:
            # Asegúrate de que cada orden tenga acceso a los productos
            order.cart_products = order.cart.products.all()
        return context


@login_required(login_url='login')
@validate_cart_and_order
def order(request, cart_cart, order):
    order = get_or_create_order(cart_cart, request)
    #request.session['order_id'] = order.id
    return render(request,'Orders/orders.html',{
        'cart_cart': cart_cart,
        'order': order,
        'breadcrumb': breadcrumb()
        
    })

@login_required(login_url='login')
@validate_cart_and_order
def address(request, cart_cart, order):
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.has_shipping_addresses()
    
    return render(request,'orders/address.html',{
        'cart': cart_cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True),
        'can_choose_address':can_choose_address,
        
    })
    
@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.addresses
    shipp_add = shipping_addresses
    return render(request,'orders/select_address.html',{
        'breadcrumb': breadcrumb(address=True),
        'shipp_add': shipp_add
    })
    
@login_required(login_url='login')
@validate_cart_and_order
def check_address(request, cart_cart, order, pk):
    
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)
    
    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')
    
    order.update_shipping_address(shipping_address)
    
    return redirect('orders:address')

@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart_cart, order):
    shipping_address  = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')
    
    return render(request,'orders/confirm.html',{
        'cart_cart': cart_cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True, confirmation=True)
    })
    
    


