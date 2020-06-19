from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin


class ViewProveedor(PermissionRequiredMixin, TemplateView):
    template_name = "proveedor.html"
    permission_required = "auth.view_user"


class ViewAdmin(PermissionRequiredMixin, TemplateView):
    template_name = "admin.html"
    permission_required = "admin.view_logentry"
