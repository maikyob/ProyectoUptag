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