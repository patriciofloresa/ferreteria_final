"""ferreteria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from apps.proveedor.views import *
from apps.users.views import *
from ferreteria.views import ListaCategorias,ListarCategorias,DetailViewProducto
from django.conf import settings
from django.conf.urls.static import static

#librerias de webpay
from tbk.services import WebpayService
from tbk.commerce import Commerce
from tbk import INTEGRACION

        
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', staff_member_required(TemplateView.as_view(template_name="index.html")),name='home'),
    path('proveedor/',ViewProveedor.as_view() ,name='proveedor_permiso'),
    path('admin_permiso/',ViewAdmin.as_view() ,name='admin_permiso'),  
    path('accounts/',include('allauth.urls')),
    path('prod/',include('apps.producto.urls')),
    path('user/',include('apps.users.urls')),
    path('cmp/',include('apps.cmp.urls')),

    path('redireccion/',TemplateView.as_view(template_name="redireccion.html"), name='redirect'),

    #url cuentas#    
    #  path('',TemplateView.as_view(template_name="inicio.html"), name='inicio'), 

     path('',ListaCategorias.as_view() ,name='inicio'),  

     path('ListarCategoria/edit/<int:pk>',ListarCategorias.as_view(),name='Listar_categorias'),

     path('Detalleproducto/<int:pk>',DetailViewProducto.as_view(),name='Detalle_Producto'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/',include(debug_toolbar.urls)),
    ] + urlpatterns
