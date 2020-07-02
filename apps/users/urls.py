from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import path
from django.views.generic import TemplateView

from .models import User
from .views import AdministrarUsuario, RegistroUsuario

app_name = "user"

urlpatterns = [
    # Urls Agregar Usuario
    #
    path('adminusuario/agregar', RegistroUsuario.as_view(), name='agregar_usuarios'),
    path('adminusuario/administrar', AdministrarUsuario.as_view(), name='admin_usuarios')

]