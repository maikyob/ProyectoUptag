from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from .form import ProductoForm, LoginForm, ServicioForm
from .models import *
from .form import ClienteForm
from django.contrib.auth.models import User
from django.contrib import messages
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
    
    return render(request, 'accounts/login.html', {'form': form})
@login_required
def salir(request):
    logout(request)
    return redirect('login')



def signup(request):
    if request.method == 'POST':
        # Aquí iría la lógica para manejar el formulario de registro
        nombre = request.POST.get('username')
        email = request.POST.get('email')
        contraseña = request.POST.get('password')
            # Lógica para crear el usuario en la base de datos
        # Evitar usuarios duplicados por email
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if User.objects.filter(email=email).exists():
            # Si existe, devolver error
            if is_ajax:
                return JsonResponse({'success': False, 'errors': 'Ese correo electrónico ya está registrado.'})
            return render(request, 'accounts/signup.html', {'error': 'Ese correo electrónico ya está registrado.'})

        if User.objects.filter(username=nombre).exists():
            # Si el nombre de usuario existe, devolver error
            if is_ajax:
                return JsonResponse({'success': False, 'errors': 'El nombre de usuario ya está en uso.'})
            return render(request, 'accounts/signup.html', {'error': 'El nombre de usuario ya está en uso.'})

        # Crear un User de Django (para poder usar authenticate/login después)
        user = User(username= nombre, email=email)
        # Guardar el nombre en first_name para mostrarlo en la plantilla
        user.first_name = nombre or ''
        user.set_password(contraseña)
        user.save()
        return redirect('login')  # Redirige al inicio de sesión después del registro
    return render(request, 'accounts/signup.html' )

#Inicio
@login_required
def index(request):
    return render(request, 'pages/home.html' )

#Urls Inventario
@login_required
def productlist(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'pages/inventario.html' , {'productos': productos} )

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('productlist')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'pages/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    nombre = producto.nombre
    producto.delete()
    messages.success(request, f'Producto "{nombre}" eliminado definitivamente.')
    return redirect('productlist')

@login_required
def addproduct(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productlist')  # Redirige a la lista de productos después de agregar
    else:
        form = ProductoForm()
    return render(request, 'pages/agregar_producto.html', {'form': form})

#Ventas
@login_required
def salelist(request):
    servicios = Servicio.objects.all()
    # Enviamos todos los productos activos por defecto
    productos = Producto.objects.filter(activo=True)
    return render(request, 'pages/ventas.html', {'servicios': servicios, 'productos': productos})
@login_required
def pos(request):
    return render(request, 'pos.html' )
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
    return render(request, 'pages/servicios.html', {'servicios': servicios})
@login_required
def addservice(request):
    if request.method == 'POST':
            form_service = ServicioForm(request.POST)
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
            if form_service.is_valid():
                servicio = form_service.save()
                
                if is_ajax:
                    return JsonResponse({'success': True, 'id': servicio.id, 'redirect': reverse('servicelist')})
                return redirect('servicelist')  # Redirige a la lista de servicios después de agregar
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
def edit_service(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form_service = ServicioForm(request.POST, instance=servicio)
        if form_service.is_valid():
            form_service.save()
            messages.success(request, 'Servicio actualizado correctamente.')
            return redirect('servicelist')
        return render(request, 'pages/editar_servicio.html', {'form_service': form_service, 'servicio': servicio})
    else:
        form_service = ServicioForm(instance=servicio)
    return render(request, 'pages/editar_servicio.html', {'form_service': form_service, 'servicio': servicio})

@login_required
def delete_service(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    servicio.delete()
    messages.success(request, 'Servicio eliminado correctamente.')
    return redirect('servicelist')

@login_required
def addpurchase(request):
    return render(request, 'addpurchase.html' )

# AJAX Views for POS
@login_required
def buscar_cliente(request):
    dni = request.GET.get('dni')
    try:
        cliente = Cliente.objects.get(dni=dni)
        return JsonResponse({
            'encontrado': True,
            'nombre': cliente.nombre,
            'email': cliente.email,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'encontrado': False})

@login_required
def get_productos_servicio(request, servicio_id):
    materiales = MaterialServicio.objects.filter(servicio_id=servicio_id).select_related('producto')
    
    if materiales.exists():
        productos = [{
            'id': m.producto.id,
            'nombre': m.producto.nombre,
            'precio': float(m.producto.precio_venta),
            'stock': m.producto.cantidad_en_stock
        } for m in materiales]
    else:
        # Fallback: Si no hay materiales vinculados, mostrar todos los productos activos
        all_prods = Producto.objects.filter(activo=True)
        productos = [{
            'id': p.id,
            'nombre': p.nombre,
            'precio': float(p.precio_venta),
            'stock': p.cantidad_en_stock
        } for p in all_prods]
        
    return JsonResponse({'productos': productos})

@login_required
@require_POST
def registrar_venta(request):
    try:
        data = json.loads(request.body)
        cliente_data = data.get('cliente')
        metodo_pago = data.get('metodo_pago')
        items = data.get('items')
        
        if not items:
            return JsonResponse({'success': False, 'error': 'No hay items en la venta'})

        with transaction.atomic():
            # 1. Obtener o crear cliente
            cliente, created = Cliente.objects.get_or_create(
                dni=cliente_data['dni'],
                defaults={
                    'nombre': cliente_data['nombre'],
                    'email': cliente_data.get('email', ''),
                    'telefono': cliente_data.get('telefono', ''),
                    'direccion': cliente_data.get('direccion', '')
                }
            )
            
            # Calcular total
            total_venta = sum(float(item['precio']) for item in items)
            
            # 2. Crear Movimiento (Venta)
            movimiento = Movimiento.objects.create(
                tipo='salida',
                total=total_venta,
                id_cliente=cliente,
                motivo=f"Venta POS ({metodo_pago})"
            )
            
            # 3. Detalles y Stock
            for item in items:
                # Si es un producto tangible (no solo un servicio)
                if item.get('producto_id'):
                    producto = Producto.objects.select_for_update().get(id=item['producto_id'])
                    if producto.cantidad_en_stock < 1:
                        raise ValueError(f"Sin stock para {producto.nombre}")
                    
                    # Descontar stock (asumiendo cantidad 1 por ahora según UI)
                    producto.cantidad_en_stock -= 1
                    producto.save()
                    
                    DetalleMovimiento.objects.create(
                        id_movimiento=movimiento,
                        id_producto=producto,
                        cantidad=1,
                        precio_unitario=item['precio']
                    )
                
                # Registrar servicio realizado
                if item.get('servicio_id'):
                    ServicioRealizado.objects.create(
                        servicio_id=item['servicio_id'],
                        fecha=movimiento.fecha.date(),
                        cliente=cliente.nombre,
                        costo=item['precio']
                    )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
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
            messages.success(request, 'Cliente agregado correctamente.')
            return redirect('clientlist')
        return render(request, 'pages/agregar_cliente.html', {'form_client': form_client})
    else:
        form_client = ClienteForm()
    return render(request, 'pages/agregar_cliente.html', {'form_client': form_client})

@login_required
def edit_client(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form_client = ClienteForm(request.POST, instance=cliente)
        if form_client.is_valid():
            form_client.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clientlist')
        return render(request, 'pages/editar_cliente.html', {'form_client': form_client, 'cliente': cliente})
    else:
        form_client = ClienteForm(instance=cliente)
    return render(request, 'pages/editar_cliente.html', {'form_client': form_client, 'cliente': cliente})

@login_required
def delete_client(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.success(request, 'Cliente eliminado correctamente.')
    return redirect('clientlist')


@login_required
def transactions(request):
    transacciones = Movimiento.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'pages/transacciones.html', {'transacciones': transacciones, 'clientes': clientes})


#Urls Perfil
@login_required
def profile(request):
    return render(request,'pages/perfil.html' )
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