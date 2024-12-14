from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
import stripe
from django.conf import settings
from django.urls import reverse
from orders.models import Order

from orders.decorators import validate_cart_and_order
from django.contrib import messages

from orders.utils import destroy_order
from carts.utils import destroy_cart

from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_PRIVATE_KEY

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, order_id=order_id)
    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        
        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.order_id,  # Usa order_id si es un UUID
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        
        # Inicializar el subtotal de los productos
        products_subtotal = 0
        
        # Accede a los productos a través del carrito asociado con la orden
        cart_products = order.cart.cartproduct_set.all()  # Usamos 'cartproduct_set' para acceder a la relación intermedia

        for cart_product in cart_products:
            product_total = cart_product.product.price * cart_product.quantity
            products_subtotal += product_total
            
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': cart_product.product.price,  # El precio en centavos
                    'currency': 'clp',
                    'product_data': {
                        'name': cart_product.product.title,  # El nombre del producto
                    },
                },
                'quantity': cart_product.quantity,
            })

        # Calcular el IVA (5% del subtotal de productos)
        iva = int(products_subtotal * 0.05)  # Multiplicado por 100 para convertir a centavos

        # Añadir el IVA como un item separado
        session_data['line_items'].append({
            'price_data': {
                'unit_amount': iva,  # IVA en centavos
                'currency': 'clp',
                'product_data': {
                    'name': 'IVA (5%)',
                },
            },
            'quantity': 1,
        })
        
        # Añadir el costo de envío como un item separado
        if order.shipping_total > 0:
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': order.shipping_total,  # El costo de envío en centavos
                    'currency': 'clp',
                    'product_data': {
                        'name': 'Costo de envío',
                    },
                },
                'quantity': 1,
            })
        
        # Crear sesión de checkout de Stripe
        session = stripe.checkout.Session.create(**session_data)
        
        # Redirigir al formulario de pago de Stripe
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())

@login_required(login_url='login')
@validate_cart_and_order
def payment_completed(request, cart_cart, order):
    
    if request.user.id != order.user_id:
        return redirect('carts:cart')
    
    order.complete()
    
    destroy_cart(request)
    destroy_order(request)
    
    messages.success(request,'Compra completada exitosamente')
    return redirect('index')


@login_required(login_url='login')
@validate_cart_and_order
def payment_canceled(request, cart_cart, order):
    
    if request.user.id != order.user_id:
        return redirect('carts:cart')
    
    order.cancel()
    destroy_cart(request)
    destroy_order(request)
    
    messages.error(request, 'Orden cancelada')
    return redirect('index')


