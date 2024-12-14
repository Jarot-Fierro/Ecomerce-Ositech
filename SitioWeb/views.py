from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegisterForm
# from django.contrib.auth.models import User
from users.models import User

from products.models import Product

from django.http import HttpResponseRedirect

# Create your views here.

from django.shortcuts import render

def mi_pagina_404(request, exception):
    return render(request, 'SitioWeb/404/404.html', status=404)


def index(request):
    products = Product.objects.all().order_by('-id')
    
    return render(request,'SitioWeb/Inicio/index.html',{
        'products': products,
    })


def view_login(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username = username, password = password)
        
        if user:
            login(request,user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])
            
            return redirect('index')
        else:
            messages.error(request,'Usuario o contraseña no validos')
        
    return render(request,'SitioWeb/Login/login.html')

def view_logout(request):
    logout(request)
    messages.success(request,'Sesión cerrada exitosamente')
    return redirect('login')

def register(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        
        user = form.save()
         
        if user:
            login(request,user)
            messages.success(request,'Usuario creado exitosamente')
            return redirect('login')
         
    return render(request,'SitioWeb/Usuarios/registro.html',{
        'form': form
    })