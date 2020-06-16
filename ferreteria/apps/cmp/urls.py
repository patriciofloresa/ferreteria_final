from django.urls import path
from apps.cmp.views import *
app_name='cmp'

urlpatterns = [
    path('ventanew/',ventaNew.as_view(),name='ventanew'),
    path('venta/list',ventaView.as_view(),name='venta_list'),
    path('despacho/',DespachoView.as_view(),name='despacho'),
    path('deleteventa',deletetodoventas.as_view(),name='ventadeleteall'),
]