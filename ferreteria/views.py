from apps.producto.models import Categoria, Producto
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView


class ListaCategorias(ListView):
    model = Categoria
    template_name = "inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_productos = Producto.objects.all()
        lista_categorias = Categoria.objects.all()

        title_page = "Inicio"
        main_title_content = "Lista de productos"
        main_subtitle_content = ""
        subtitle_table = ""

        context.update({
            'CLASS_MENU_INICIO': "active",
            'CLASS_SUBMENU_INICIO': "show",
            'CLASS_SUBMENU_INICIO_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
            'prod': lista_productos,
            'cat': lista_categorias,
        })
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
