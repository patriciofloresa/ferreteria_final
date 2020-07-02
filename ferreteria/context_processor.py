from apps.producto.models import Categoria


def informacion_global(request):
    return {"categorias": Categoria.objects.all()}
