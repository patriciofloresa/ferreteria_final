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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte_ventas_mensual'] = self.get_reporte_ventas_mensual()
        context.update({            
            'monto_total_ventas': self.busca_monto_total_ventas(),
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'precio_maximo': self.busca_precio_maximo(),
            'precio_minimo': self.busca_precio_minimo(),            
        })
        return context
    
    


    
    
        
        


