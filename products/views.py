from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from products.models import Product

from django.db.models import Q
# Create your views here.
class ProductListView(ListView):
    template_name = 'SitioWeb/Inicio/index.html'
    queryset = Product.objects.all().order_by('-id')
    paginate_by = 8
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = context['product_list']
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'Productos/product.html'
    

class ProductSearchListView(ListView):
    template_name = 'Productos/search.html'
    
    def get_queryset(self):
        filters = Q(title__icontains = self.query()) | Q(category__title__icontains = self.query())
        # SELECT * FROM products WHERE title like %valor%
        return Product.objects.filter(filters)
    
    def query(self):
        return self.request.GET.get('q')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()
        return context
    
def index_list_product(request):
    
    return render(request,'SitioWeb/Inicio/index_list_product.html',{
        
    })