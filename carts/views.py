from django.shortcuts import render, redirect
from .models import Cart
from .utils import get_or_create_cart
from products.models import Product
from django.contrib import messages

from django.shortcuts import get_object_or_404

from .models import CartProduct
# Create your views here.


def cart(request):
    cart = get_or_create_cart(request)
    cart_all_products = cart     ## Los valores de cart no se ven reflejados en el template, el name causa conflicto
    return render(request, 'Carts/cart.html', {
        'cart_all_products':cart_all_products
    })


def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk= request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))
    
    if int(quantity) < 1:
        quantity = 1
    cart_product = CartProduct.objects.create_or_update_quantity(cart=cart , product= product, quantity=quantity)
    
    return render(request, 'Carts/add.html', {
        'quantity': quantity,
        'cart_product': cart_product,
        'product': product
    })


def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk= request.POST.get('product_id'))
    
    cart.products.remove(product)
    
    return redirect('carts:cart')
