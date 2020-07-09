# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AbstractUser
# Redireccionar al sitio
from django.urls import reverse_lazy
from django.shortcuts import render

#Mensajes en django
from django.contrib import messages
#Redirecciones en djando
from django.shortcuts import redirect, render, reverse

#importando modelos y forms a utilizar
from .forms import CoreSignupForm, RegistrarEmpleado, EditarEmpleado
from .models import User
from django.views.generic import (ListView,CreateView,DeleteView,UpdateView)
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def contacto(request):

    return render(request, "gracias.html")

class RegistroUsuario(LoginRequiredMixin,CreateView):
    model = User
    template_name = 'adminusuario/agregar.html'
    form_class = RegistrarEmpleado
    success_url=reverse_lazy("user:admin_usuarios")
    def get_success_url(self):
        messages.success(self.request, 'Se ha registrado exitosamente el usuario : {}'.format(self.object.first_name))
        return reverse('user:admin_usuarios', kwargs={})


class AdministrarUsuario(LoginRequiredMixin,ListView):
    model = User
    template_name = 'adminusuario/administrar.html'
    context_object_name="usuarios"
    ordering = ["-date_joined"]
    paginate_by = 10

class EditarUsuario(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "adminusuario/editar.html"
    form_class = EditarEmpleado
    context_object_name = "usuarios"
    success_url = reverse_lazy("user:admin_usuarios")
    def get_success_url(self):
        messages.success(self.request, 'Se ha modificado exitosamente el usuario : {}'.format(self.object.first_name))
        return reverse('user:admin_usuarios', kwargs={})
    
    
    def form_valid(self, form):
        clean = form.cleaned_data 
        context = {}        
        self.object = form.save()
        return super(EditarUsuario, self).form_valid(form)  
    
