from django.contrib import messages

from apps.cmp.forms import VentaForm
from apps.cmp.models import Carrito, CarritoProducto, Categoria, Producto, venta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

# Create your views here.


class Listarallventas(DetailView):
    def post(self, request, *args, **kwargs):
        todocarrito = CarritoProducto.objects.filter(
            carrito__usuario=self.request.user.id)
        for i in todocarrito:
            i.save()
        return HttpResponseRedirect(reverse("cmp:venta_list"))


class ventaNew(LoginRequiredMixin, FormView):
    model = venta, CarritoProducto,Producto
    template_name = "carritoproducto/ventanew.html"
    form_class = VentaForm
    success_url = reverse_lazy("cmp:venta_list")
    login_url = "/accounts/login/"

    def post(self, request, *args, **kwargs):
        venta_carrito = venta.objects.filter(carrito=self.request.POST['carrito'])
        if len(venta_carrito) > 0:
            messages.warning(self.request, 'Ya se registro un carrito')
            return HttpResponseRedirect(reverse('cmp:venta_list'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        carrito_producto = CarritoProducto.objects.filter(
            carrito__usuario=self.request.user.id
        )
        formulario = form.save(commit=False)
        # formulario.carrito = Carrito.objects.get(usuario_id=self.request.user.id)
        formulario.estado = "orden completada"
        suma_temp = 0
        for x in formulario.carrito.detalles.all():
            suma_temp += x.producto.precio * x.cantidad
            print("Sotck ", x.producto.stock)
            x.producto.actualizarStock(x.cantidad*-1)
            x.producto.save()
            print("Nuevo : ", x.producto.stock)
        print(suma_temp)
        formulario.precio = suma_temp
        formulario.save()
        return super().form_valid(form)


class ventaView(LoginRequiredMixin, ListView):
    permission_required = "prod.view_categoria"
    model = venta
    template_name = "carritoproducto/ventalist.html"
    context_object_name = "ven"
    login_url = "/accounts/login/"


class DespachoView(TemplateView):
    template_name = "carritoproducto/despacho.html"


class deletetodoventas(View):
    def post(self, request, *args, **kwargs):
        #
        venta.objects.all().delete()
        return HttpResponseRedirect(reverse("cmp:venta_list"))


class ventaDelete(LoginRequiredMixin, DeleteView):
    model = venta
    template_name = "carritoproducto/delete.html"
    context_object_name = "venta"
    success_url = reverse_lazy("cmp:venta_list")
    login_url = "/accounts/login/"


class detailventa(LoginRequiredMixin,DeleteView):
    template_name = "carritoproducto/venta.html"
    model = venta,CarritoProducto
    context_object_name = 'ventadetalle'
    queryset = venta.objects.all()
    print(queryset)


