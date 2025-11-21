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
# --- Endpoint AJAX para buscar cliente por DNI ---
def buscar_cliente(request):
    dni = request.GET.get('dni', '').strip()
    data = {'encontrado': False}
    if dni:
        cliente = Cliente.objects.filter(dni=dni).first()
        if cliente:
            data = {
                'encontrado': True,
                'nombre': cliente.nombre,
                'email': cliente.email,
                'telefono': cliente.telefono,
                'direccion': cliente.direccion,
            }
    return JsonResponse(data)
from django.contrib.auth import authenticate, login, logout
from .form import ProductoForm
from .form import ClienteForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .form import ServicioForm
from .models import *
# Create your views here.

#Autenticacion
def signin(request):
    if request.method == 'POST':
        # Aquí iría la lógica para manejar el formulario de inicio de sesión
        user = authenticate(
            request, 
            username=request.POST.get('email'), 
            password=request.POST.get('contraseña'))
        # Si la petición es AJAX (fetch/jQuery), devolver JSON
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if user is None:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': 'Credenciales inválidas'})
            return render(request, 'pages/Login.html', {'error': 'Credenciales inválidas'})

        # Usuario válido
        login(request, user)
        if is_ajax:
            return JsonResponse({'success': True, 'redirect': '/'})
        return redirect('/')  # Redirige a la página principal después del inicio de sesión
        
    return render(request, 'pages/Login.html' )
def signup(request):
    if request.method == 'POST':
        # Aquí iría la lógica para manejar el formulario de registro
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
            # Lógica para crear el usuario en la base de datos
        # Evitar usuarios duplicados por email
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if User.objects.filter(username=email).exists():
            # Si existe, devolver error
            if is_ajax:
                return JsonResponse({'success': False, 'errors': 'Usuario ya registrado con ese correo.'})
            return render(request, 'pages/register.html', {'error': 'Usuario ya registrado con ese correo.'})

        # Crear un User de Django (para poder usar authenticate/login después)
        user = User(username= nombre, email=email)
        # Guardar el nombre en first_name para mostrarlo en la plantilla
        user.first_name = nombre or ''
        user.set_password(contraseña)
        user.save()

        # Guardar en modelo local `usuario` (opcional). Guardamos contraseña hasheada.
        from django.contrib.auth.hashers import make_password
        nuevo_usuario = usuario(nombre=nombre, email=email, contraseña=make_password(contraseña))
        nuevo_usuario.save()

        if is_ajax:
            return JsonResponse({'success': True, 'redirect': '/signin/'})

        return redirect('signin')  # Redirige al inicio de sesión después del registro
    return render(request, 'pages/register.html' )

#Inicio
def index(request):
    return render(request, 'pages/home.html' )

#Urls Inventario
def productlist(request):
    productos = Producto.objects.all()
    return render(request, 'pages/inventario.html' , {'productos': productos} )

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

def salelist(request):
    servicios = Servicio.objects.all()
    return render(request, 'pages/ventas.html', {'servicios': servicios})

def pos(request):
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'pos.html' , {'productos': productos, 'servicios': servicios, 'clientes': clientes})

def salesreturnlist(request):
    return render(request, 'salesreturnlist.html' )

def createsalesreturn(request):
    return render(request, 'createsalesreturn.html' )

#Servicios

def servicelist(request):
    servicios = Servicio.objects.all()
    return render(request, 'pages/servicios.html'  , {'servicios': servicios} )

def addservice(request):
    if request.method == 'POST':
            form_service = ServicioForm(request.POST)
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
            if form_service.is_valid():
                servicio = form_service.save()
                messages.success(request, 'Servicio agregado correctamente.')
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

def importpurchase(request):
    return render(request, 'importpurchase.html' )

#Clientes

def clientlist(request):
    clientes = Cliente.objects.all()
    return render(request,'pages/clientlist.html' , {'clientes': clientes} )

def addclient(request):
    if request.method == 'POST':
        form_client = ClienteForm(request.POST)
        if form_client.is_valid():
            form_client.save()
            messages.success(request, 'Cliente agregado correctamente.')
            return redirect('clientlist')  # Redirige a la lista de clientes después de agregar
        # Si el formulario no es válido, volver a mostrar con errores
        return render(request, 'pages/agregar_cliente.html', {'form_client': form_client})
    else:
        form_client = ClienteForm()
    return render(request, 'pages/agregar_cliente.html', {'form_client': form_client})

#Urls Perfil

def profile(request):
    return render(request,'pages/perfil.html' )

#Url Transacciones

def transactions(request):
    return render(request, 'pages/transacciones.html')

def Hello(request):
    return HttpResponse("Hola")

def about(request):
    return HttpResponse("About")

