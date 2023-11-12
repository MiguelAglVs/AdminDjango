from django import forms
from django.forms import ModelForm
from .models import Persona
from datetime import date, timedelta


class PersonForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'eps': forms.Select(attrs={'class': 'form-select'}),
            'discapacidad': forms.Select(attrs={'class': 'form-select'}),
            'diagnostico': forms.Select(attrs={'class': 'form-select'}),
        }
        exclude = ['user']

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            edad = (date.today() - fecha_nacimiento) // timedelta(days=365.25)
            if not (0.33 <= edad <= 10):
                raise forms.ValidationError(
                    "La edad debe estar entre 4 meses y 10 años.")
        return fecha_nacimiento
