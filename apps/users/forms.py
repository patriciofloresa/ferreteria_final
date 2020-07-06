from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
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

    class Meta:
        model = User
        fields = [
            'rut',
            'first_name',
            'last_name',
            'celular',
            'email',
            'cargo',
            'password1',
            'password2',
            'is_staff',
            'is_active',
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})

class EditarEmpleado(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'rut',
            'first_name',
            'last_name',
            'celular',
            'email',
            'cargo',
            'is_staff',
            'is_active'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
              
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})

    
            
    
    
        
    
