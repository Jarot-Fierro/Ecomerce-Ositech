from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'price', 'image','brand', 'material', 'gender', 'country_origin', 'clothing_model')
    list_display = ('__str__', 'slug', 'create_at')

admin.site.register(Product,ProductAdmin)



    
    
    
    