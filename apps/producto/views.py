from apps.users.models import User
from django.contrib import messages

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

# Redireccionar al sitio
from django.urls import reverse_lazy

# Importamos la clases genericas
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

# Importamos la categoria form
from .forms import CategoriaForm, MarcaForm, ProductoForms, TipoProductoForm

# Importamos los modelos
from .models import Carrito, CarritoProducto, Categoria, Marca, Producto, TipoProducto
from django.contrib import messages

# Creamos La marca
from ..cmp.models import venta


class MarcaView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "prod.view_categoria"
    model = Marca
    template_name = "Marcas/marcalist.html"
    context_object_name = "marca"
    login_url = "/accounts/login/"


class MarcaNew(LoginRequiredMixin, CreateView):
    model = Marca
    template_name = "Marcas/marca_form.html"
    form_class = MarcaForm
    success_url = reverse_lazy("prod:marca_list")
    login_url = "/accounts/login/"


class MarcaEditar(LoginRequiredMixin, UpdateView):
    model = Marca
    template_name = "Marcas/marca_edit.html"
    form_class = MarcaForm
    context_object_name = "marca"
    success_url = reverse_lazy("prod:marca_list")
    login_url = "/accounts/login/"


class MarcaDelete(LoginRequiredMixin, DeleteView):
    model = Marca
    template_name = "Marcas/marca_delete.html"
    context_object_name = "marca"
    success_url = reverse_lazy("prod:marca_list")
    login_url = "/accounts/login/"


class deletetodoMarca(View):
    def post(self, request, *args, **kwargs):
        #
        TipoProducto.objects.all().delete()
        return HttpResponseRedirect(reverse("prod:marca_list"))


# Creamos la vista de categoria
class CategoriaView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "prod.view_categoria"
    model = Categoria
    template_name = "categoria/list.html"
    context_object_name = "categoria"
    login_url = "/accounts/login/"


class CategoriaNew(LoginRequiredMixin, CreateView):
    model = Categoria
    template_name = "categoria/categoria_form.html"
    form_class = CategoriaForm
    success_url = reverse_lazy("prod:categoria_list")
    login_url = "/accounts/login/"


class CategoriaEditar(LoginRequiredMixin, UpdateView):
    model = Categoria
    template_name = "categoria/categoria_edit.html"
    form_class = CategoriaForm
    context_object_name = "categoria"
    success_url = reverse_lazy("prod:categoria_list")
    login_url = "/accounts/login/"


class CategoriaDelete(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = "categoria/categoria_delete.html"
    context_object_name = "categoria"
    success_url = reverse_lazy("prod:categoria_list")
    login_url = "/accounts/login/"


class deletetodoCategoria(View):
    def post(self, request, *args, **kwargs):
        #
        Categoria.objects.all().delete()
        return HttpResponseRedirect(reverse("prod:categoria_list"))


# Creamos las Vista de Tipo De Producto
class TipoProductoView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "prod.view_tipoproducto"
    model = TipoProducto
    template_name = "tipo_producto/tipo_productolist.html"
    context_object_name = "obj"
    login_url = "/accounts/login/"


class TipoProductoNew(LoginRequiredMixin, CreateView):
    model = TipoProducto
    template_name = "tipo_producto/tipo_productoForm.html"
    form_class = TipoProductoForm
    success_url = reverse_lazy("prod:tipoproducto_list")
    login_url = "/accounts/login/"


class TipoProductoEditar(LoginRequiredMixin, UpdateView):
    model = TipoProducto
    template_name = "tipo_producto/tipoproducto_edit.html"
    form_class = TipoProductoForm
    context_object_name = "obj"
    success_url = reverse_lazy("prod:tipoproducto_list")
    login_url = "/accounts/login/"


class TipoProductoDelete(LoginRequiredMixin, DeleteView):
    model = TipoProducto
    template_name = "tipo_producto/tipo_productodelete.html"
    context_object_name = "obj"
    success_url = reverse_lazy("prod:tipoproducto_list")
    login_url = "/accounts/login/"


class deletetodoTipoProducto(View):
    def post(self, request, *args, **kwargs):
        #
        TipoProducto.objects.all().delete()
        return HttpResponseRedirect(reverse("prod:tipoproducto_list"))


# Creamos las vista de producto
class ProductoView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "producto/producto_list.html"
    context_object_name = "product"
    login_url = "/accounts/login/"


class ProductoNew(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "prod.view_producto"
    model = Producto
    template_name = "producto/producto_form.html"
    form_class = ProductoForms
    success_url = reverse_lazy("prod:producto_list")
    login_url = "/accounts/login/"


class ProductoEditar(LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = "producto/producto_edit.html"
    context_object_name = "product"
    form_class = ProductoForms
    success_url = reverse_lazy("prod:producto_list")
    login_url = "/accounts/login/"


class ProductoDelete(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "producto/producto_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("prod:producto_list")
    login_url = "/accounts/login/"


def añadircarrito(request, idproducto):
    cantidad = int(request.POST["cantidad"])
    try:
        carrito = Carrito.objects.get(usuario=request.user, estatus="open")
    except:
        carrito = Carrito.objects.create(usuario=request.user)
        request.session["carritopk"] = carrito.pk

    carrito_producto, creado = CarritoProducto.objects.get_or_create(
        producto=Producto.objects.get(pk=idproducto), carrito=carrito
    )
    carrito_producto.cantidad = carrito_producto.cantidad + cantidad
    carrito_producto.save()

    return redirect("prod:detallecarrito", pk=carrito.pk)


class ListCarritoView(DetailView):
    model = Carrito
    queryset = Carrito.objects.filter(estatus="abierto")
    template_name = "MostrarProductos/Carrito.html"

    def get_object(self, queryset=None):
        try:
            return super.get_object(queryset)
        except:
            carrito_usuario = Carrito.objects.filter(
                usuario=self.request.user, estatus="open"
            )
            if len(carrito_usuario) == 0:
                carrito = Carrito(usuario=self.request.user)
                carrito.save()
                return carrito
            else:
                return carrito_usuario[0]


list_carrito_view = ListCarritoView.as_view()

# Elimina todo de un carrito
class deletetodocarrito(View):
    def post(self, request, *args, **kwargs):
        #
        CarritoProducto.objects.all().delete()
        return HttpResponseRedirect(reverse("inicio"))


# Elimina todo de un producto
class deletetodoProducto(View):
    def post(self, request, *args, **kwargs):
        #
        Producto.objects.all().delete()
        return HttpResponseRedirect(reverse("prod:producto_list"))


def deleteCarrito(request, pk):
    cat = Categoria.objects.all()
    carrito = CarritoProducto.objects.filter(pk=pk)
    carrito.delete()
    return render(request, "MostrarProductos/Carrito.html")


class DeleteCartShopping(DeleteView):
    model = CarritoProducto
    template_name = "MostrarProductos/Carrito.html"

    def get_success_url(self):
        return self.request.META["HTTP_REFERER"]


delete_cart_shopping = DeleteCartShopping.as_view()


class UpdateCarrito(UpdateView):
    model = Carrito
    fields = ("estatus",)

    def get_success_url(self):
        messages.success(self.request, "Muchas gracias por la compra")
        return "/"

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            venta_carrito=venta(carrito=self.get_object(),comuna="",direccion="",precio=self.get_object().get_total(),estado="",ciudad="")
            venta_carrito.save()
            carrito = self.get_object()
            carrito.estatus = "pagado"
            carrito.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
    

    

update_carrito = UpdateCarrito.as_view()