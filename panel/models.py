from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Eps(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre

class Diagnostico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre

class Discapacidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre

class Imagen(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='img/', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.imagen.url

class Persona(models.Model):
    dni = models.CharField(max_length=10, primary_key=True,null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    apellido_materno = models.CharField(max_length=50, null=False)
    fecha_nacimiento = models.DateField(null=False)
    eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
    discapacidad = models.ForeignKey(Discapacidad, on_delete=models.CASCADE)
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def calcular_edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

