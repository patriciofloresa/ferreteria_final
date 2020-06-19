from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from .views import RegistroUsuario, AdministrarUsuario
from .models import User

app_name = "user"

urlpatterns = [
    # Urls Agregar Usuario
    #
    path(
        "adminusuario/agregar",
        login_required(RegistroUsuario.as_view()),
        name="agregar_usuarios",
    ),
    path(
        "adminusuario/administrar", AdministrarUsuario.as_view(), name="admin_usuarios"
    ),
]
