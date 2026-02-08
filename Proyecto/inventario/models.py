from django.db import models
# Create your models here.

class usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    contraseña = models.CharField(max_length=100)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_en_stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)



class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class ServicioRealizado(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    cliente = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    
class MaterialServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
class Movimiento(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('salida', 'Salida'), ('ajuste', 'Ajuste')])
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)  # Para entradas
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)      # Para salidas
    motivo = models.CharField(max_length=200)

class DetalleMovimiento(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
