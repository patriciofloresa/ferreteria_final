from django import forms
from django.forms import ModelForm
from apps.abastecimiento.models import Pedido
from apps.producto.models import Producto
from apps.users.models import User


class PedidoForm(ModelForm):
    # campos adicionales del detalle
    producto = forms.ChoiceField(required=False)
    precio = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '0'}))
    cantidad = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '0'}))
    subtotal = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '0'}))

    proveedores = User.objects.filter(cargo="Proveedor").order_by('username')
    lista_temp = [('', '-- seleccione --')]
    lista_temp.extend([(x.id, x.username) for x in proveedores])

    list_productos = Producto.objects.all().order_by('Nombre')
    lista_temp_productos = [('', '-- seleccione --')]
    lista_temp_productos.extend([(x.pk, '({}) | {}'.format(x.codigo, x.Nombre)) for x in list_productos])

    lista_documentos = [('', '-- seleccione --'), ('FACTURA', 'Factura')]

    class Meta:
        model = Pedido
        exclude = ['estado', 'usuario']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
            })
        self.fields['numero'].widget.attrs['autofocus'] = True
        self.fields['proveedor'].choices = self.lista_temp
        self.fields['producto'].choices = self.lista_temp_productos
        self.fields['tipo_documento'].choices = self.lista_documentos
        self.fields['total'].widget.attrs['class'] = 'form-control text-right'
        self.fields['total'].widget.attrs['readonly'] = 'readonly'


class PedidoDetailForm(ModelForm):

    class Meta:
        model = Pedido
        exclude = ['estado', 'usuario']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
                'readonly': 'readonly',
            })
