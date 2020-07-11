from django import forms

# Importamos el modelo al cual queremos acceder.
from .models import Categoria, Marca, Producto, TipoProducto, Carrito
# Realizamos el formularios de las categorias ...
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["Nombre"]  # Que quieres que se muestre
        labels = {"nombre": "Nombre de la categoria"}
        widget = {"Nombre": forms.TextInput}  # Darle estilo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})
    
    #Validacion del Nombre
    # def clean_Nombre(self):
    #     Nombre= self.cleaned_data['Nombre']
    #     if not Nombre.isalpha():
    #         print('Nombre',Nombre)
    #         raise forms.ValidationError("No se puede ingresar un tipo de valor Numerico")
    #     return Nombre


# Definimos El forms De tipo de Producto
class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ["categoria", "Nombre", "Um"]
        labels = {"nombre": "Nombre de producto"}
        widget = {"Nombre": forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["categoria"].empty_label = "Seleccione Categoria"
        self.fields["Nombre"].widget.attrs.update(
            {"placeholder": " Nombre del tipo de Producto"}
        )
        self.fields["Um"].widget.attrs.update(
            {"placeholder": " Ingrese Unidad de medida"}
        )

    #Validacion de categoria
    def clean_categoria(self):
        categoria =self.cleaned_data['categoria']
        if categoria == '':
            raise forms.ValidationError("No puede estar el campo Vacio")
        return categoria

    # def clean_Nombre(self):
    #     Nombre =self.cleaned_data['Nombre']
    #     if not Nombre.isalpha():
    #         print('Nombre',Nombre)
    #         raise forms.ValidationError("No se puede ingresar un tipo de valor Numerico")
    #     return Nombre
#Validamos el tipo de producto



# Definimos El forms de producto


class ProductoForms(forms.ModelForm):
    class Meta:
        model = Producto  # Seleccionamos el producto en el cual queremos acceder
        fields = [
            "Nombre",
            "codigo",
            "precio",
            "descripcion",
            "marca",
            "color",
            "stock",
            "id_proveedor",
            "imagen",
            "Categoria",
            "TipoProducto",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields["Nombre"].widget.attrs.update(
                {"placeholder": " Nombre del Producto"}
            )
            self.fields["codigo"].widget.attrs.update(
                {"placeholder": " Ingrese codigo"}
            )
            self.fields["stock"].widget.attrs.update({"placeholder": " Stock"})
            self.fields["descripcion"].widget.attrs.update(
                {"placeholder": " Descripcion"}
            )
            self.fields["color"].widget.attrs.update({"placeholder": "Ingrese color"})
            self.fields["imagen"].widget.attrs.update({"id": "ImagenTxt"})

# #Validacion de codigo
#     def clean_codigo(self):
#             codigo =self.cleaned_data['codigo']
#             if codigo <= 0:
#                 raise forms.ValidationError("No puede ingresar un valor igual o inferior a 0")
#                 return codigo
#             else:
#                 return codigo
      
#Validacion del stock
    def clean_stock(self):
        stock =self.cleaned_data['stock']
        if stock <= 0:
            raise forms.ValidationError("No puede ingresar un valor igual o inferior a 0")
            return stock
        else:
            return stock

#Validacion del precio
    def clean_precio(self):
        precio =self.cleaned_data['precio']
        if precio <= 0:
            raise forms.ValidationError("No puede ingresar un valor igual o inferior a 0")
            return precio
        else:
            return precio

#Validacion de Nombre 
    # def clean_Nombre(self):
    #     Nombre =self.cleaned_data['Nombre']
    #     if not Nombre.isalpha():
    #         raise forms.ValidationError("No se puede ingresar un dato de valor Numerico")
    #     return Nombre

#Validacion de color
    # def clean_color(self):
    #     color=self.cleaned_data['color']
    #     if not color.isalpha():
    #         raise forms.ValidationError("No se puede ingresar un dato de valor Numerico")
    #     return color
    
#Validacion de descripcion
    # def clean_descripcion(self):
    #     descripcion=self.cleaned_data['descripcion']
    #     if not descripcion.isalpha():
    #         raise forms.ValidationError("No se puede ingresar un dato de valor Numerico")
    #     return descripcion


# Realizamos el formulario de Marca
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ["nombre"]  # Que quieres que se muestre
        labels = {"nombre": "Nombre de la Marca"}
        widget = {"nombre": forms.TextInput}  # Darle estilo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})
            
    # def clean_nombre(self):
    #     nombre= self.cleaned_data['nombre']
    #     if not nombre.isalpha():
    #         raise forms.ValidationError("No se puede ingresar un tipo de valor Numerico")
    #     return nombre
    
    




class CarritoPagarForm(forms.ModelForm):

    sede_desc = forms.CharField(widget=forms.TextInput(), required=False)

    class Meta:
        model = Carrito
        exclude = ['usuario', 'estatus', 'monto_total']

