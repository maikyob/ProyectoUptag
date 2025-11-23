from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .form import ProductoForm
from .models import usuario
from .models import Producto
from django.contrib.auth.models import User
from django.db import IntegrityError

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
        try:
            usuario = User.objects.create_user(username=nombre, email=email, password=contraseña, first_name=nombre)
            print(request.POST)
            login(request, usuario)
            return redirect('signin')
        except IntegrityError as e: 
            print(e)
    return render(request, 'pages/register.html',)

def signout(request):
    logout(request)
    return redirect('signin')

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
            form.save()
            return redirect('productlist')  # Redirige a la lista de productos después de agregar
    else:
        form = ProductoForm()
    return render(request, 'pages/agregar_producto.html', {'form': form})

#Ventas

def salelist(request):
    return render(request, 'pages/ventas.html' )

def pos(request):
    return render(request, 'pos.html' )

def salesreturnlist(request):
    return render(request, 'salesreturnlist.html' )

def createsalesreturn(request):
    return render(request, 'createsalesreturn.html' )

#Compras

def purchaselist(request):
    return render(request, 'purchaselist.html' )

def addpurchase(request):
    return render(request, 'addpurchase.html' )

def importpurchase(request):
    return render(request, 'importpurchase.html' )

#Expensas

def expenselist(request):
    return render(request,'expenselist.html' )

def addexpense(request):
    return render(request,'addexpense.html' )

def expensecategory(request):
    return render(request,'expensecategory.html' )

#Urls Perfil

def profile(request):
    return render(request,'pages/perfil.html' )

def Hello(request):
    return HttpResponse("Hola")

def about(request):
    return HttpResponse("About")

