from django import forms
from .models import Producto, Cliente, usuario, Servicio

# Formulario para el modelo Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio_compra", "precio_venta", "cantidad_en_stock", "proveedor"]

# Formulario para el modelo Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

# Formulario para el modelo Servicio
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = "__all__"

# Formulario para el modelo usuario (Registro)
class RegisterForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = "__all__"

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Ingresa tu usuario',
            'autocomplete': 'username'
        }),
        label="USUARIO",
        max_length=100
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password'
        }),
        label="PASSWORD"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': 'Ingresa tu usuario',
            'autocomplete': 'username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password'
        })