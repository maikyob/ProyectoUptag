from django.views.decorators.csrf import csrf_exempt
# --- Endpoint para registrar venta ---
import json
@csrf_exempt
def registrar_venta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente_data = data.get('cliente', {})
            metodo_pago = data.get('metodo_pago')
            items = data.get('items', [])
            # Buscar o crear cliente
            cliente, _ = Cliente.objects.get_or_create(dni=cliente_data.get('dni'), defaults={
                'nombre': cliente_data.get('nombre'),
                'email': cliente_data.get('email'),
                'telefono': cliente_data.get('telefono'),
                'direccion': cliente_data.get('direccion'),
            })
            # Calcular total de la venta
            total_venta = sum(float(item.get('precio', 0)) * int(item.get('cantidad', 1)) for item in items)
            # Crear movimiento de salida (venta)
            movimiento = Movimiento.objects.create(
                tipo='salida',
                total=total_venta,
                id_cliente=cliente,
                motivo=f'Venta - Método de pago: {metodo_pago}'
            )
            # Registrar cada producto vendido
            for item in items:
                producto = Producto.objects.filter(nombre=item.get('producto')).first()
                cantidad = int(item.get('cantidad', 1))
                precio = float(item.get('precio', 0))
                if producto:
                    DetalleMovimiento.objects.create(
                        id_movimiento=movimiento,
                        id_producto=producto,
                        cantidad=cantidad,
                        precio_unitario=precio
                    )
                    # Actualizar stock
                    producto.cantidad_en_stock = max(producto.cantidad_en_stock - cantidad, 0)
                    producto.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
from django.views.decorators.http import require_GET
# AJAX: productos por servicio
@require_GET
def productos_por_servicio(request):
    servicio_id = request.GET.get('servicio_id')
    productos = []
    if servicio_id:
        materiales = MaterialServicio.objects.filter(servicio_id=servicio_id).select_related('producto')
        for mat in materiales:
            productos.append({
                'id': mat.producto.id,
                'nombre': mat.producto.nombre,
                'precio': float(mat.producto.precio_venta)
            })
    return JsonResponse({'productos': productos})
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, authenticate
from .form import ProductoForm
from .form import ClienteForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .form import ServicioForm, LoginForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeView,PasswordChangeDoneView

# Create your views here.

#Autenticacion

def login_view(request): 
    if request.method == 'POST': 
        form = LoginForm(request.POST) 
        if form.is_valid(): 
            # Validar el usuario y la contraseña 
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password'] 
            user = authenticate(username=username, password=password) 
            if user is not None: 
                login(request, user) 
                return redirect('/') 
            else: 
                form.add_error(None, "Nombre de usuario o contraseña incorrectos.")   
        else: 
            # Verificar si hay errores específicos del formulario
            if form.errors:
                # Si hay errores de campos específicos, mostrarlos
                for field, errors in form.errors.items():
                    if field != '__all__':
                        for error in errors:
                            form.add_error(field, error)
            else:
                form.add_error(None, "Por favor, verifica los datos ingresados.") 
    else: 
        form = LoginForm() 
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def signin(request):
    if request.method == 'POST':
        # Aquí iría la lógica para manejar el formulario de inicio de sesión
        usuario = authenticate(
            request, 
            username=request.POST.get('email'), 
            password=request.POST.get('contraseña'))
        if usuario is None:
            return render(request, 'pages/Login.html', {'error': 'Credenciales inválidas'})
        else:
            login(request, usuario)
            return redirect('/')
    return render(request, 'pages/Login.html' )
def signup(request):
    if request.method == 'POST':
        # Aquí iría la lógica para manejar el formulario de registro
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        try:
            usuario = User.objects.create_user(username=email, email=email, password=contraseña, first_name=nombre)
            usuario.save()
            print(request.POST)
            return redirect('signin')
        except IntegrityError as e: 
            print(e)
    return render(request, 'pages/register.html',)

def signout(request):
    logout(request)
    return redirect('signin')

#Inicio
@login_required
def index(request):
    return render(request, 'pages/home.html' )

#Urls Inventario
@login_required
def productlist(request):
    productos = Producto.objects.all()
    return render(request, 'pages/inventario.html' , {'productos': productos} )
@login_required
def addproduct(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            # Registrar el producto en MaterialServicio para todos los servicios existentes
            servicios = Servicio.objects.all()
            for servicio in servicios:
                MaterialServicio.objects.create(servicio=servicio, producto=producto, cantidad=1)
            return redirect('productlist')
    else:
        form = ProductoForm()
    return render(request, 'pages/agregar_producto.html', {'form': form})

#Ventas

@login_required
def salelist(request):
    servicios = Servicio.objects.all()
    return render(request, 'pages/ventas.html', {'servicios': servicios})

@login_required
def pos(request):
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'pos.html' , {'productos': productos, 'servicios': servicios, 'clientes': clientes})

@login_required
def salesreturnlist(request):
    return render(request, 'salesreturnlist.html' )

@login_required
def createsalesreturn(request):
    return render(request, 'createsalesreturn.html' )

#Servicios

@login_required
def servicelist(request):
    servicios = Servicio.objects.all()
    return render(request, 'pages/servicios.html'  , {'servicios': servicios} )

@login_required
def addservice(request):
    if request.method == 'POST':
            form_service = ServicioForm(request.POST)
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
            if form_service.is_valid():
                servicio = form_service.save()
                
                if is_ajax:
                    return JsonResponse({'success': True, 'id': servicio.id, 'redirect': '/servicelist'})
                return redirect('/servicelist')  # Redirige a la lista de servicios después de agregar
            # Si el formulario no es válido, devolver errores JSON para AJAX o renderizar plantilla
            if is_ajax:
                # serialize form errors
                errors = {field: [str(e) for e in errs] for field, errs in form_service.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            # include products for select price option
            productos = Producto.objects.all()
            return render(request, 'pages/agregar_servicio.html', {'form_service': form_service, 'productos': productos})
    else:
        form_service = ServicioForm()
    productos = Producto.objects.all()
    return render(request, 'pages/agregar_servicio.html', {'form_service': form_service, 'productos': productos})

@login_required
def importpurchase(request):
    return render(request, 'importpurchase.html' )

#Clientes

@login_required
def clientlist(request):
    clientes = Cliente.objects.all()
    return render(request,'pages/clientlist.html' , {'clientes': clientes} )

@login_required
def addclient(request):
    if request.method == 'POST':
        form_client = ClienteForm(request.POST)
        if form_client.is_valid():
            form_client.save()
            
            return redirect('clientlist')  # Redirige a la lista de clientes después de agregar
        # Si el formulario no es válido, volver a mostrar con errores
        return render(request, 'pages/agregar_cliente.html', {'form_client': form_client})
    else:
        form_client = ClienteForm()
    return render(request, 'pages/agregar_cliente.html', {'form_client': form_client})

#Urls Perfil

@login_required
def profile(request):
    return render(request,'pages/perfil.html' )

#Url Transacciones

@login_required
def transactions(request):
    transaccion = Movimiento.objects.all()
    cliente = Cliente.objects.all()
    return render(request, 'pages/transacciones.html', {'transaccion': transaccion, 'cliente': cliente})

@login_required
def Hello(request):
    return HttpResponse("Hola")

@login_required
def about(request):
    return HttpResponse("About")

#ACCOUNTS
class CustomPasswordResetView(PasswordResetView):
    template_name="accounts/password_reset.html"
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name="accounts/password_reset_done.html"
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name="accounts/password_reset_confirm.html"
    def form_valid(self, form): 
    # Comprueba si el token es válido 
        if self.validlink: 
            return super().form_valid(form) 
        else: 
            # Renderiza la plantilla con un mensaje de error 
            context = self.get_context_data() 
            context['validlink'] = False 
            return render(self.request, self.template_name, context) 
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name="accounts/password_reset_complete.html"
    
class CustomPasswordChangeView(PasswordChangeView):
    template_name="accounts/password_change.html"
    
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name="accounts/password_change_done.html"