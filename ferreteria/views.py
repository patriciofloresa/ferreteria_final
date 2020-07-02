from apps.producto.models import Categoria, Producto
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView



class ListaCategorias(ListView):
    model = Categoria
    template_name = "inicio.html"
     

    def get_context_data(self, **kwargs):
        # context = super(ListarRubros, self).get_context_data(**kwargs)
        context = {}
        context_object_name = "cat"
        context_object_name = "prod"
        prod = Producto.objects.all()
        context["prod"] = prod
        cat = Categoria.objects.all()
        print("inicio")
        context["cat"] = cat
        return context
        


class ListarCategorias(ListView):
    model = Producto
    template_name = "MostrarProductos/Producto.html"
    # context_object_name='cat'

    def get_queryset(self):
        cate = Producto.objects.filter(Categoria=self.kwargs["pk"])
        return cate

    def get_context_data(self, **kwargs):
        context = super(ListarCategorias, self).get_context_data(**kwargs)
        context_object_name = "cat"
        categoryall = Categoria.objects.all()
        context["cat"] = categoryall
        return context


class DetailViewProducto(DetailView):
    model = Producto
    template_name = "MostrarProductos/detalleproducto.html"

    def get_context_data(self, **kwargs):
        context = super(DetailViewProducto, self).get_context_data(**kwargs)
        context_object_name = "cat"
        categoryall = Categoria.objects.all()
        context["cat"] = categoryall
        return context
