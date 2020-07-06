# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render

# Redireccionar al sitio
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.shortcuts import render
#Redireccionar al sitio
from django.urls import reverse_lazy
#Permisos
from django.contrib.auth.mixins import LoginRequiredMixin

#importando modelos y forms a utilizar
from .forms import CoreSignupForm, RegistrarEmpleado, EditarEmpleado
from .models import User
from django.views.generic import (ListView,CreateView,DeleteView,UpdateView)
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


class RegistroUsuario(LoginRequiredMixin,CreateView):
    model = User
    template_name = 'adminusuario/agregar.html'
    form_class = RegistrarEmpleado
    success_url=reverse_lazy("user:admin_usuarios")


class AdministrarUsuario(LoginRequiredMixin,ListView):
    model = User
    template_name = 'adminusuario/administrar.html'
    context_object_name="usuarios"
    ordering = ["-date_joined"]
    paginate_by = 10

class EliminarUsuario(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "adminusuario/eliminar.html"
    context_object_name = "usuarios"
    success_url = reverse_lazy("user:admin_usuarios")

class EditarUsuario(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "adminusuario/editar.html"
    form_class = EditarEmpleado
    context_object_name = "usuarios"
    success_url = reverse_lazy("user:admin_usuarios")
    
    
    def form_valid(self, form):
        clean = form.cleaned_data 
        context = {}        
        self.object = form.save()
        return super(EditarUsuario, self).form_valid(form)  
    
