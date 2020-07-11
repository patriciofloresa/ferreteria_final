from apps.cmp.views import *
from apps.cmp.reportes import *
from django.urls import path

app_name = "cmp"

urlpatterns = [
    path("ventadelete/<int:pk>",ventaDelete.as_view(),name="ventadelete"),
    path("ventanew/", ventaNew.as_view(), name="ventanew"),
    path("venta/list", ventaView.as_view(), name="venta_list"),

    #Despacho de ventas.
    path("deleteventa", deletetodoventas.as_view(), name="ventadeleteall"),
    path("allventa", Listarallventas.as_view(), name="ventaall"),
    path("detailview/<int:pk>", detailventa.as_view(), name="detailventa"),
    #Url de reportes.
    path('ventas/listadoreportes',reportes_compras,name="ventas_print_all"),
]