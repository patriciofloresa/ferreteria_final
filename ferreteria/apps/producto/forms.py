from django import forms
# Importamos el modelo al cual queremos acceder.
from .models import Categoria, TipoProducto, Producto, Marca

# Realizamos el formularios de las categorias ...


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['Nombre']  # Que quieres que se muestre
        labels = {'nombre': 'Nombre de la categoria'}
        widget = {'Nombre': forms.TextInput}  # Darle estilo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


# Definimos El forms De tipo de Producto
class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ['categoria', 'Nombre', 'Descripcion', 'Um']
        labels = {'nombre': 'Nombre de producto'}
        widget = {'Nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['categoria'].empty_label = "Seleccione Categoria"
        self.fields['Nombre'].widget.attrs.update({
            'placeholder': ' Nombre del tipo de Producto'
        })
        self.fields['Descripcion'].widget.attrs.update({
            'placeholder': ' Descripcion Producto'
        })
        self.fields['Um'].widget.attrs.update({
            'placeholder': ' Ingrese Unidad de medida'
        })

# Definimos El forms de producto


class ProductoForms(forms.ModelForm):
    class Meta:
        model = Producto  # Seleccionamos el producto en el cual queremos acceder
        fields = ['Nombre', 'codigo', 'precio', 'descripcion', 'marca', 'color',
                  'Stock', 'id_proveedor', 'imagen', 'Categoria', 'TipoProducto']
        widget = {'Nombre': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['Nombre'].widget.attrs.update({
                'placeholder': ' Nombre del Producto'
            })
            self.fields['codigo'].widget.attrs.update({
                'placeholder': ' Ingrese codigo'
            })
            self.fields['Stock'].widget.attrs.update({
                'placeholder': ' Stock'
            })
            self.fields['descripcion'].widget.attrs.update({
                'placeholder': ' Descripcion'
            })
            self.fields['color'].widget.attrs.update({
                'placeholder': 'Ingrese color'
            })



#Realizamos el formulario de Marca

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']  # Que quieres que se muestre
        labels = {'nombre': 'Nombre de la Marca'}
        widget = {'nombre': forms.TextInput}  # Darle estilo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
