import json
from django_ajax.decorators import ajax
from django.db.models import Q, Sum, Count, Max, Min
from django.db.models.functions import Coalesce 
from django.db import connection
from apps.cmp.models import venta
from django.shortcuts import render
#datetime para conesuir el año actual
from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title_page = "Inicio | Dashboard"
        main_title_content = "Dashboard"
        title="Usuarios del sistema"
        main_subtitle_content = ""
        subtitle_table = ""
        context['total_ventas'] = self.busca_monto_total_ventas()
        context.update({
            'CLASS_MENU_DASHBOARD': "menu-open",
            'CLASS_SUBMENU_DASHBOARD': "active",
            'CLASS_SUBMENU_DASHBOARD_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'title':title,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'producto_mas_vendidos':self.producto_mas_vendidos(),
            'precio_maximo': self.busca_precio_maximo(),
            'precio_minimo': self.busca_precio_minimo(),
            'evolucion_ventas': self.busca_evolucion_ventas(),
            'cant_item_x_categorias': self.busca_cant_item_x_categorias(),
        })
        return context

    def busca_monto_total_ventas(self):
        data = []
        try:
            total = venta.objects.aggregate(r=Coalesce(Sum('precio'),0)).get('r')
            data = total
        except Exception as e:
            print("Error: {}".format(e))
        return data
    
    def busca_cant_total_ventas(self):
        data = []
        try:
            total = venta.objects.aggregate(r=Coalesce(Count('id'),0)).get('r')
            data = total
        except Exception as e:
            print("Error: {}".format(e))
        return data
        
    def busca_precio_maximo(self):
        data = []   
        try:
            data = venta.objects.aggregate(r=Coalesce(Max('precio'),0)).get('r')
        except:
             data = [0]
        return data

    def busca_precio_minimo(self):
        data = []   
        try:
            data = venta.objects.aggregate(r=Coalesce(Min('precio'),0)).get('r')
        except:
             data = [0]
        return data

    def busca_evolucion_ventas(self):
        dict_meses = {
            '01': 0,
            '02': 0,
            '03': 0,
            '04': 0,
            '05': 0,
            '06': 0,
            '07': 0,
            '08': 0,
            '09': 0,
            '10': 0,
            '11': 0,
            '12': 0
        }
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                    select to_char(fc,'mm') from cmp_venta order by fc asc;
                """
            )
            for row in cursor.fetchall():
                mes = row[0]    # mes
                dict_meses[mes] = row[1]    # total
            return json.dumps(dict_meses)
        except Exception as e:
            print("Error: {}".format(e))

    def busca_cant_item_x_categorias(self):
        dict_categorias = {}
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                select * from (        
                select pc.Nombre ,sum(producto_carritoproducto.cantidad) 
                from 
                cmp_venta,producto_carritoproducto,producto_producto, producto_categoria pc
                where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                and producto_producto.codigo = producto_carritoproducto.producto_id
                and pc.id = producto_producto.Categoria_id 
                group by pc.Nombre  
                order by sum(producto_carritoproducto.cantidad) desc
                )
where rownum < 4;
                
                """
            )
            for row in cursor.fetchall():
                dict_categorias.update({row[0]: row[1]})
            return json.dumps(dict_categorias)
        except Exception as e:
            print("Error: {}".format(e))
    
    
    def producto_mas_vendidos(self):
        dict_producto = {}
        try:
            cursor= connection.cursor()
            cursor.execute(
                """
                select producto_producto.Nombre,sum(producto_carritoproducto.cantidad) 
                from 
                cmp_venta,producto_carritoproducto,producto_producto
                where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                and producto_producto.codigo = producto_carritoproducto.producto_id 
                group by producto_producto.Nombre  
                order by sum(producto_carritoproducto.cantidad) desc
                limit 3
                ;
                """
            )
            for row in cursor.fetchall():
                dict_producto.update({row[0]: row[1]})
            return json.dumps(dict_producto) 
        except Exception as e:
            print("Error: {}".format(e))
