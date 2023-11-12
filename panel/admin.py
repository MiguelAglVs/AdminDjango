from django.contrib import admin
from .models import *


class EpsAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


class DiscapacidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


class ImagenAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_creacion',)
    list_display = ('id', 'imagen', 'user', 'fecha_creacion')


class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'apellido_materno',
                    'fecha_nacimiento', 'eps', 'discapacidad', 'diagnostico', 'user')


# Register your models here.
admin.site.register(Eps, EpsAdmin)
admin.site.register(Diagnostico, DiagnosticoAdmin)
admin.site.register(Discapacidad, DiscapacidadAdmin)
admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Persona, PersonaAdmin)
