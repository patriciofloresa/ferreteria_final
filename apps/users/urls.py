from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import path
from django.views.generic import TemplateView

from .models import User
from .views import AdministrarUsuario, RegistroUsuario, EliminarUsuario, EditarUsuario

app_name = "user"

urlpatterns = [
    # Urls Agregar Usuario
    #
    path('adminusuario/agregar', RegistroUsuario.as_view(), name='agregar_usuarios'),
    path('adminusuario/administrar', AdministrarUsuario.as_view(), name='admin_usuarios'),
    path('adminusuario/eliminar/<int:pk>', EliminarUsuario.as_view(), name='eliminar_usuario'),
    path('adminusuario/editar/<int:pk>/', EditarUsuario.as_view(), name='editar_usuario'),

]