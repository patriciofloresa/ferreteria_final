from django.shortcuts import render
#Redireccionar al sitio
from django.urls import reverse_lazy
#Permisos
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#importando modelos y forms a utilizar
from .forms import CoreSignupForm, RegistrarEmpleado
from .models import User
from django.views.generic import (ListView,CreateView,DeleteView,UpdateView)
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class RegistroUsuario(CreateView):
        model = User
        template_name = 'adminusuario/agregar.html'
        form_class = RegistrarEmpleado
        success_url=reverse_lazy("user:agregar_usuarios")


class AdministrarUsuario(LoginRequiredMixin,ListView,UpdateView, DeleteView):
        model = User
        template_name = 'adminusuario/administrar.html'
        form_class = CoreSignupForm
        context_object_name="obj"
        success_url=reverse_lazy("user:administrar")
        login_url="/accounts/login/"


# def register(request):
#         if request.method('POST'):
#                 form = RegistrarEmpleado(request.POST)                
#                 return redirect('adminusuario/agregar')
#         else:
#                 form = RegistrarEmpleado()
#                 args = {'form': form}
#         return render(request, 'adminusuario/agregar', args)
    



