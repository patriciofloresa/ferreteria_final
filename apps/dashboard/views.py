import json
import cx_Oracle
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

connection = cx_Oracle.connect('it/it@127.0.0.1:1521/orcl')
cursor = connection.cursor()

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte_ventas_mensual'] = self.get_reporte_ventas_mensual()
        context['venta_min_por_mes'] = self.get_venta_min_por_mes()
        context['venta_max_por_mes'] = self.get_venta_max_por_mes()
        context['cant_max_mensual'] = self.get_cant_max_mensual()
        context['nombre_max_mensual'] = self.get_nombre_max_mensual()
        context['mes_max_mensual'] = self.get_mes_max_mensual()
        # context['nombre_categoria']    = self.get_nombre_categoria()
        context['monto_total_ventas'] = self.busca_monto_total_ventas()
        context.update({  
            'nombre_categoria': self.get_nombre_categoria(),
            'cantidad_categoria': self.get_cantidad_categoria(),
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'precio_maximo': self.busca_precio_maximo(),
            'precio_minimo': self.busca_precio_minimo(),            
        })
        return context


    def get_reporte_ventas_mensual(self):
        data = []   
        try:
            year = datetime.now().year               
            for m in range(1,13):
                total = venta.objects.filter(fc__year = year, fc__month = m ).aggregate(r=Coalesce(Sum('precio'),0)).get('r')
                data.append(total)
        except:
             data = [0]
        return data
    
    def get_venta_min_por_mes(self):
        data = []   
        try:
            year = datetime.now().year               
            for m in range(1,13):
                total = venta.objects.filter(fc__year = year, fc__month = m ).aggregate(r=Coalesce(Min('precio'),0)).get('r')
                data.append(total)
        except:
             data = [0]
        return data

    def get_venta_max_por_mes(self):
        data = []   
        try:
            year = datetime.now().year               
            for m in range(1,13):
                total = venta.objects.filter(fc__year = year, fc__month = m ).aggregate(r=Coalesce(Max('precio'),0)).get('r')
                data.append(total)
        except:
             data = [0]
        return data

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
            total = venta.objects.aggregate(r=Coalesce(Count('precio'),0)).get('r')
            data = total
            return data
        except Exception as e:
            print("Error: {}".format(e))
        return data

    def busca_precio_maximo(self):
        data = []
        try:
            total = venta.objects.aggregate(r=Coalesce(Max('precio'),0)).get('r')
            data = total
        except Exception as e:
            print("Error: {}".format(e))
        return data

    def busca_precio_minimo(self):
        data = []
        try:
            total = venta.objects.aggregate(r=Coalesce(Min('precio'),0)).get('r')
            data = total    
        except Exception as e:
            print("Error: {}".format(e))
        return data
     
    def get_cant_max_mensual(self):
        qs = """
            select  venta_maxima from (       
                    select extract(month from cmp_venta.fc)as mes,producto_producto.nombre as nombre, max(producto_carritoproducto.cantidad) as venta_maxima
                    from 
                    cmp_venta,producto_carritoproducto,producto_producto, producto_categoria pc
                    where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                    and producto_producto.codigo = producto_carritoproducto.producto_id
                    and pc.id = producto_producto.Categoria_id 
                    group by extract(month from cmp_venta.fc), producto_producto.nombre
                    order by sum(producto_carritoproducto.cantidad) desc
                    )
            where rownum <13
            group by nombre, venta_maxima, mes
            order by mes desc,venta_maxima desc
            """
        cursor.execute(qs)
        item = cursor.fetchall()
        return json.dumps(item)

    def get_nombre_max_mensual(self):
        qs = """
        
            select  nombre from (       
                    select extract(month from cmp_venta.fc)as mes,producto_producto.nombre as nombre, max(producto_carritoproducto.cantidad) as venta_maxima
                    from 
                    cmp_venta,producto_carritoproducto,producto_producto, producto_categoria pc
                    where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                    and producto_producto.codigo = producto_carritoproducto.producto_id
                    and pc.id = producto_producto.Categoria_id 
                    group by extract(month from cmp_venta.fc), producto_producto.nombre
                    order by sum(producto_carritoproducto.cantidad) desc
                    )
            where rownum <13
            group by nombre, venta_maxima, mes
            order by mes desc,venta_maxima desc
            """
        cursor.execute(qs)
        item = cursor.fetchall()
        return json.dumps(item)

    def get_nombre_categoria(self):   
        qs = """ select * from (        
                select pc.Nombre 
                from 
                cmp_venta,producto_carritoproducto,producto_producto, producto_categoria pc
                where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                and producto_producto.codigo = producto_carritoproducto.producto_id
                and pc.id = producto_producto.Categoria_id 
                group by pc.Nombre  
                order by sum(producto_carritoproducto.cantidad) desc)
                where rownum < 4 """
        cursor.execute(qs)  
        item = cursor.fetchall()
        # list_item = []
        # for i in item:
        #     list_item.append(i)
        return json.dumps(item)

    def get_cantidad_categoria(self):
        qs = """ select * from (        
                select sum(producto_carritoproducto.cantidad)
                from 
                cmp_venta,producto_carritoproducto,producto_producto, producto_categoria pc
                where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                and producto_producto.codigo = producto_carritoproducto.producto_id
                and pc.id = producto_producto.Categoria_id 
                group by pc.Nombre  
                order by sum(producto_carritoproducto.cantidad) desc)
                where rownum < 4 """
        cursor.execute(qs)
        item = cursor.fetchall()
        # list_item = []
        # for i in item:
        #     list_item.append(i)
        return json.dumps(item)
    
    def get_mes_max_mensual(self):
        qs = """
            select  mes from (       
                    select extract(month from cmp_venta.fc)as mes,producto_producto.nombre as nombre, max(producto_carritoproducto.cantidad) as venta_maxima
                    from 
                    cmp_venta,producto_carritoproducto,producto_producto, producto_categoria pc
                    where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                    and producto_producto.codigo = producto_carritoproducto.producto_id
                    and pc.id = producto_producto.Categoria_id 
                    group by extract(month from cmp_venta.fc), producto_producto.nombre
                    order by sum(producto_carritoproducto.cantidad) desc
                    )
            where rownum <13
            group by nombre, venta_maxima, mes
            order by mes desc,venta_maxima desc
            """
        cursor.execute(qs)
        item = cursor.fetchall()
        return json.dumps(item)    
    
        
        
    
    
    


    
    
        
        


