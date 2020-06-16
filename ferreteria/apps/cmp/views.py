from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from apps.cmp.forms import VentaForm
from apps.cmp.models import venta,CarritoProducto,Carrito,Producto,Categoria
from django.views.generic import (ListView,CreateView,DeleteView,UpdateView,DetailView,FormView,TemplateView,View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
# Create your views here.

class ventaNew(LoginRequiredMixin,FormView):
    model=venta,CarritoProducto
    template_name="carritoproducto/ventanew.html"
    form_class=VentaForm 
    success_url=reverse_lazy("cmp:venta_list")
    login_url="/accounts/login/"
    
    def form_valid(self,form):
        carrito_producto=CarritoProducto.objects.filter(carrito__usuario=self.request.user.id)
        formulario = form.save(commit=False)
        formulario.carrito=Carrito.objects.get(usuario_id=self.request.user.id)
        formulario.estado='orden completada'
        sumaprecio=carrito_producto.aggregate(Sum('producto__precio'))
        print(sumaprecio)
        formulario.precio=sumaprecio['producto__precio__sum']
        formulario.save()
        return super().form_valid(form)

class ventaView(LoginRequiredMixin ,ListView):
    permission_required ="prod.view_categoria"
    model = venta  
    template_name="carritoproducto/ventalist.html"
    context_object_name="ven"
    login_url="/accounts/login/"


class DespachoView(TemplateView):
    template_name="carritoproducto/despacho.html"


class deletetodoventas(View):
    def post(self, request, *args, **kwargs):
    #
        venta.objects.all().delete()
        return HttpResponseRedirect(
            reverse(
                'cmp:venta_list'
            )
        )

