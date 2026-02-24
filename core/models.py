from django.db import models

# Create your models here.

class Empresa(models.Model):
    nombre = models.CharField(max_length=150)
    cuit = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True) #blank=True permite que el campo sea opcional
    telefono = models.CharField(max_length=30, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50, choices = [
        ('admin', 'Administrador'),
        ('tecnico', 'Técnico'),
        ('consulta', 'Solo consulta'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.empresa.nombre}"
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"


