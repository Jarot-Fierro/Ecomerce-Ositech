
from django.contrib import admin
from django.urls import path
from SitioWeb import views

from django.urls import include

from products.views import ProductListView

from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls import handler404


from django.urls import re_path
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('',ProductListView.as_view(),name='index'),
    path('usuarios/login',views.view_login,name='login'),
    path('usuarios/logout',views.view_logout,name='logout'),
    path('usuarios/registro',views.register,name='register'),
    path('producto/',include('products.urls')),
    path('carrito/',include('carts.urls')),
    path('orden/', include('orders.urls')),
    path('direcciones/', include('shipping_addresses.urls')),
    path('codigos/', include('promo_codes.urls')),
    path('payment/', include('payment.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)