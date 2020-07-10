import json
from django_ajax.decorators import ajax
from django.db.models import Q, Sum, Count, Max, Min
from django.db.models.functions import Coalesce 
from django.db import connection
from apps.cmp.models import venta
from apps.producto.models import Categoria
from django.shortcuts import render
#datetime para conesuir el año actual
from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    #Obtenemos el reporte de ventas mensual con el framework de django
    def get_reporte_ventas_mensual(self):
        data = []   
        try:
            year = datetime.now().year               
            for m in range(1,13):
                total = venta.objects.filter(fc__year = year, fc__month = m).aggregate(r=Coalesce(Sum('precio'),0)).get('r')
                data.append(total)
        except:
             data = [0]
        return data

    def get_reporte_venta_minima_mensual(self):
        data = []   
        try:
            year = datetime.now().year               
            for m in range(1,13):
                total = venta.objects.filter(fc__year = year, fc__month = m).aggregate(r=Coalesce(Min('precio'),0)).get('r')
                data.append(total)
        except:
             data = [0]
        return data    

    def get_reporte_venta_maxima_mensual(self):
        data = []   
        try:
            year = datetime.now().year               
            for m in range(1,13):
                total = venta.objects.filter(fc__year = year, fc__month = m).aggregate(r=Coalesce(Max('precio'),0)).get('r')
                data.append(total)
        except:
             data = [0]
        return data
    #Obtenemos el reporte de ventas y comparamos su valor en %
    def get_cantidad_por_categoria(self):
        data = [1]
        # try:
        #     item = venta.objects.all()
        #     for item in venta
        #         total= 
        # except: 
        #     pass
        return data
    
    def get_nombre_categoria(self):
        data = []
        for nombre in Categoria.objects.values_list('Nombre'):
            categoria = Categoria.objects.values('Nombre').aggregate()
            data.append(categoria)
        return data

    #Obtenemos valor total de las ventas en el mes con el framework de django
    def busca_monto_total_ventas(self):
        data = []
        try:
            total = venta.objects.aggregate(r=Coalesce(Sum('precio'),0)).get('r')
            data = total
        except Exception as e:
            print("Error: {}".format(e))
        return data

    #Obtenemos la cantidad total de las ventas mensual con el framework de django
    def busca_cant_total_ventas(self):
        data = []
        try:
            total = venta.objects.aggregate(r=Coalesce(Count('precio'),0)).get('r')
            data = total
        except Exception as e:
            print("Error: {}".format(e))
        return data

    #Obtenemos el valor máximo de una venta mensual con el framework de django
    def busca_precio_maximo(self):
        data = []
        try:
            total = venta.objects.aggregate(r=Coalesce(Max('precio'),0)).get('r')
            data = total
        except Exception as e:
            print("Error: {}".format(e))
        return data

    #Obtenemos el valor minimo de una venta mensual con el framework de django
    def busca_precio_minimo(self):
        data = []
        try:
            total = venta.objects.aggregate(r=Coalesce(Min('precio'),0)).get('r')
            data = total    
        except Exception as e:
            print("Error: {}".format(e))
        return data
    #Enviamos la data obtenida a travéz de un context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte_ventas_mensual'] = self.get_reporte_ventas_mensual()
        context['cantidad_por_categoria'] = self.get_cantidad_por_categoria()
        context['nombre_categoria'] = self.get_nombre_categoria()
        context.update({  
            'reporte_venta_minima_mensual': self.get_reporte_venta_minima_mensual(),
            'reporte_venta_maxima_mensual': self.get_reporte_venta_maxima_mensual(),         
            'monto_total_ventas': self.busca_monto_total_ventas(),
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'precio_maximo': self.busca_precio_maximo(),
            'precio_minimo': self.busca_precio_minimo(),            
        })
        return context
    
    


    
    
        
        


