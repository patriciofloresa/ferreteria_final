from django.urls import path

from . import views
from .views import (
    CategoriaDelete,
    CategoriaEditar,
    CategoriaNew,
    CategoriaView,
    MarcaDelete,
    MarcaEditar,
    MarcaNew,
    MarcaView,
    ProductoDelete,
    ProductoEditar,
    ProductoNew,
    ProductoView,
    TipoProductoDelete,
    TipoProductoEditar,
    TipoProductoNew,
    TipoProductoView,
    delete_cart_shopping,
    deletetodocarrito,
    deletetodoCategoria,
    deletetodoMarca,
    deletetodoProducto,
    deletetodoTipoProducto,
    update_carrito,
    ListCarritoView,
)

# Le asignamos un nombre a la app
app_name = "prod"

urlpatterns = [
    # Urls Marca
    path("marca/list", MarcaView.as_view(), name="marca_list"),
    path("marca/new", MarcaNew.as_view(), name="marca_new"),
    path("marca/edit/<int:pk>", MarcaEditar.as_view(), name="marca_edit"),
    path("marca/Delete/<int:pk>", MarcaDelete.as_view(), name="marca_Delete"),
    path("deleallmarca", deletetodoMarca.as_view(), name="deletetodomarca"),
    # Urls Categorias
    path("categorias/list", CategoriaView.as_view(), name="categoria_list"),
    path("categorias/new", CategoriaNew.as_view(), name="categoria_new"),
    path("categorias/edit/<int:pk>", CategoriaEditar.as_view(), name="categoria_edit"),
    path("categorias/Delete/<int:pk>", CategoriaDelete.as_view(), name="categoria_Delete"),
    path("deleteallcategoria", deletetodoCategoria.as_view(), name="deletetodocategoria"),
    # Urls Tipo de Producto
    path("TipoProducto/list", TipoProductoView.as_view(), name="tipoproducto_list"),
    path("TipoProducto/new", TipoProductoNew.as_view(), name="tipoproducto_new"),
    path("TipoProducto/edit/<int:pk>", TipoProductoEditar.as_view(),name="tipoproducto_edit",),
    path("TipoProducto/Delete/<int:pk>", TipoProductoDelete.as_view(), name="TipoProducto_delete", ),
    path("delealltipoproducto", deletetodoTipoProducto.as_view(), name="deletetodotipoproducto",
    ),
    # Urls Productos.
    path("Producto/list", ProductoView.as_view(), name="producto_list"),
    path("Producto/new", ProductoNew.as_view(), name="producto_new"),
    path("Producto/edit/<str:pk>", ProductoEditar.as_view(), name="Producto_edit"),
    path("Producto/Delete/<str:pk>", ProductoDelete.as_view(), name="Producto_delete"),
    path("Productodeletetodo", deletetodoProducto.as_view(), name="productodeletetodo"),
    # Urls Carrito
    path("update/<int:pk>/", update_carrito, name="updatecarrito"),
    path("añadircarrito/<int:idproducto>/", views.añadircarrito, name="carrito"),
    path("detallecarrito/<int:pk>/", ListCarritoView.as_view(), name="detallecarrito"),
    path("removercarrito/<int:pk>/", delete_cart_shopping, name="removercarrito"),
    path("deleteall/", deletetodocarrito.as_view(), name="deleteall"),
]
