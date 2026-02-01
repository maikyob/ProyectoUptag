from django import forms

# Formulario para el modelo Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        from .models import Producto
        model = Producto
        fields = "__all__"

# Formulario para el modelo usuario
class RegisterForm(forms.Form):
       class Meta:
           from .models import usuario
           model = usuario
           fields = "__all__"


# Formulario para el modelo Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        from .models import Cliente
        model = Cliente
        fields = "__all__"


# Formulario para el modelo Servicio
class ServicioForm(forms.ModelForm):
    class Meta:
        from .models import Servicio
        model = Servicio
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
        
        # Asegurar que los campos tengan las clases correctas
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