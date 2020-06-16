from django import forms
from .models import venta

class VentaForm(forms.ModelForm):
    class Meta:
        model = venta
        fields = ['carrito'] # Que quieres que se muestre
        # labels = {'nombre': 'Nombre de la categoria'}
        # widget = {'Nombre': forms.TextInput}  # Darle estilo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

