from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Colonia(models.Model):
    codigo_postal = models.CharField(max_length=10)
    nombre_colonia = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    fechas = models.DateField(auto_now_add=True)
    ESTADO_OPCIONES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='ACTIVO')

    def __str__(self):
        return self.nombre_colonia

class Cuadrilla(models.Model):
    numero_cuadrilla = models.IntegerField()
    jefe_cuadrilla = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jefes_cuadrilla', limit_choices_to={'rol': 'JEFE DE CUADRILLA'})
    fechas = models.DateField(auto_now_add=True)
    ESTADO_OPCIONES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='ACTIVO')

    def __str__(self):
        return str(self.numero_cuadrilla)

class EmpleadoCuadrilla(models.Model):
    cuadrilla = models.ForeignKey('Cuadrilla', on_delete=models.CASCADE, related_name='empleados')
    empleado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'rol': 'EMPLEADO'})

    class Meta:
        unique_together = ('cuadrilla', 'empleado')

class Usuario(AbstractUser):
    ROL_OPCIONES=[
        ('ADMINISTRADOR','administrador'),
        ('JEFE DE CUADRILLA','jefe de cuadrilla'),
        ('EMPLEADO','empleado')
    ]
    rol = models.CharField(max_length=50,choices=ROL_OPCIONES, default='EMPLEADO')
    identificacion = models.CharField(max_length=20, unique=True)
    fecha = models.DateField(auto_now_add=True)
    ESTADO_OPCIONES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='ACTIVO')

class Actividad(models.Model):
    nombre_actividad = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='actividad_imagenes/')
    detalles = models.TextField()
    ESTADO_OPCIONES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='ACTIVO')
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jefesde_cuadrillas', limit_choices_to={'rol': 'JEFE DE CUADRILLA'})
    id_colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    id_cuadrilla = models.ForeignKey(Cuadrilla, on_delete=models.CASCADE)
    

