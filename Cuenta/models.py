from django.db import models
from django.db.models.deletion import CASCADE

class Persona(models.Model):
    carnet_identidad = models.PositiveIntegerField(primary_key=True)
    nombre           = models.CharField(max_length=50)
    apellido         = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    ciudad           = models.CharField(max_length=15)
    email            = models.EmailField(max_length=80, unique=True)
    contraseña       = models.CharField(max_length=50)
    telefono         = models.IntegerField()
    domicilio        = models.CharField(max_length=50)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nombre
    
    class Meta:
        abstract = True


class Usuario(Persona):
    
    def __str__(self):
        return self.nombre

