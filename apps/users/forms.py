from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm

from .models import *


class CoreSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, label="Primer Nombre")
    last_name = forms.CharField(max_length=50, label="Apellidos")
    rut = forms.CharField(max_length=50, label="Documento")
    celular = forms.CharField(max_length=50, label="Documento")

    def custom_signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.rut = self.cleaned_data["rut"]
        user.celular = self.cleaned_data["celular"]
        user.cargo = "Cliente"
        user.save()
        group = Group.objects.get(name="Cliente")
        user.groups.add(group)
        return user

    def clean_rut(self):

        rut = self.cleaned_data.get("rut")

        # Para Validar mayusculas y minusculas
        qs = User.objects.filter(rut__iexact=rut)

        if qs.exists():
            raise forms.ValidationError("El documento se encuentra repetido")
        return rut

    def clean_celular(self):

        celular = self.cleaned_data.get("celular")

        # Para Validar mayusculas y minusculas
        qs = User.objects.filter(celular__iexact=celular)

        if qs.exists():
            raise forms.ValidationError("El Celular se encuentra repetido")
        return celular


class RegistrarEmpleado(UserCreationForm):
    direccion = forms.CharField(max_length=50, label='Direccion')

    class Meta:
        model = User
        fields = [
            'rut',
            'first_name',
            'last_name',
            'celular',
            'email',
            'cargo',
            'direccion',
            'password1',
            'is_staff',
            'is_superuser',
            ]
        labels = {

            'rut': 'rut',
            'first_name':'nombre',
            'last_name':'apellido',
            'celular':  'celular contacto',
            'email':    'correo',
            'cargo':    'cargo',
            'direccion':'direccion',
            'password1':'Contraseña',
            'is_staff': 'es empleado ?',
            'is_superuser':'será administrador?'
        }
