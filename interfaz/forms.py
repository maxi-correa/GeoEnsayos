from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from ensayos.models import Obra
import re


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su usuario"
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su contraseña"
        })
    )

class ObraForm(forms.ModelForm):

    class Meta:
        model = Obra
        fields = [
            'nombre',
            'numero_expediente',
            'tipo_contratacion',
            'numero_licitacion',
            'ubicacion',
            'contratista',
            'fecha_inicio',
        ]

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label}"
            })
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Obra.objects.filter(nombre=nombre).exists():
            raise ValidationError("Ya existe una obra con este nombre.")
        return nombre
