from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .enumeraciones import *
from django.contrib.auth.models import AbstractUser


# MODELO USUARIO
class User(AbstractUser):
    rut=models.CharField(max_length=10, null=True)
    direccion=models.CharField(max_length=500, null=True)
    celular=models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(999999999)], null=False)
    postal=models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(9999999)], null=False)


# MODELO CATEGORIA
class Categoria(models.Model):
    descripcion = models.CharField(max_length=200, null=False)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Descripcion: {self.descripcion}"

# MODELO PRODUCTO
class Producto(models.Model):
    nombre=models.CharField(max_length=50, null=False)
    descripcion=models.CharField(max_length=100, null=False)
    foto=models.ImageField(upload_to='personas',null=True)
    precio=models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cantidad_disponible = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, related_name="productos")

    def __str__ (self):
        return f"{self.id} -  {self.nombre} {self.descripcion}"
    
# MODELO CARRITO
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito", blank=True, null=True)
    total = models.DecimalField(default=0,null=False, max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Usuario_id: {self.usuario.id if self.usuario else 'Anónimo'} | Total: {self.total}"

# MODELO DETALLE DEL CARRITO
class Carrito_item(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Producto: {self.producto.nombre} | Carrito_id: {self.carrito.id}"


# MODELO REGISTRO
class Registro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    productos = models.ManyToManyField('Producto', through='RegistroItem')
    rut = models.CharField(max_length=10, null=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

# MODELO DEL DETALLE DEL REGISTRO
class RegistroItem(models.Model):
    compra = models.ForeignKey(Registro, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_producto
        super().save(*args, **kwargs)
