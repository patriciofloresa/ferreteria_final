"""ferreteria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from apps.users.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from ferreteria.views import DetailViewProducto, ListaCategorias, ListarCategorias

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("apps.dashboard.urls")),
    path("home/abastecimiento/", include("apps.abastecimiento.urls")),

    path("accounts/", include("allauth.urls")),
    path("prod/", include("apps.producto.urls")),
    path("user/", include("apps.users.urls")),
    path("cmp/", include("apps.cmp.urls")),

    path("redireccion/", TemplateView.as_view(template_name="redireccion.html"), name="redirect"),

    path("", ListaCategorias.as_view(), name="inicio"),
    path("ListarCategoria/edit/<int:pk>", ListarCategorias.as_view(), name="Listar_categorias"),
    path("Detalleproducto/<int:pk>", DetailViewProducto.as_view(), name="Detalle_Producto"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
