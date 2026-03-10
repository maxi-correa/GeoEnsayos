from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from ensayos.models import Obra, Contratista, Ubicacion
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
            'activa',
        ]

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # checkbox
            if name == 'activa':
                field.widget.attrs.update({
                    'class': 'form-check-input',
                })
            # resto de inputs
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': f"Ingrese {field.label}"
                })
        
        self.fields["numero_expediente"].initial = "XXXX-M-XXXX"
        self.fields["numero_licitacion"].initial = "XX/XX-SIOySP"
        self.fields["ubicacion"].queryset = Ubicacion.objects.filter(activa=True).order_by('nombre')
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()

        queryset = Obra.objects.filter(nombre=nombre)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise ValidationError("Ya existe una obra con este nombre.")
        
        return nombre
    
    def clean_numero_expediente(self):
        expediente = self.cleaned_data['numero_expediente'].upper()

        queryset = Obra.objects.filter(numero_expediente=expediente)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise ValidationError("Ya existe una obra con este número de expediente.")
        
        return expediente
    
    def clean_numero_licitacion(self):
        licitacion = self.cleaned_data['numero_licitacion']

        queryset = Obra.objects.filter(numero_licitacion=licitacion)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise ValidationError("Ya existe una obra con este número de licitación.")
        
        return licitacion
    
class ContratistaForm(forms.ModelForm):
    class Meta:
        model = Contratista
        fields = ['nombre', 'cuit', 'direccion', 'email', 'telefono', 'logo', 'activa']

        def clean_nombre(self):
            nombre = self.cleaned_data['nombre'].upper()

            qs = Contratista.objects.filter(nombre__iexact=nombre)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError("Ya existe un contratista con este nombre.")
            
            return nombre
        
        def clean_cuit(self):
            cuit = self.cleaned_data['cuit']

            if not cuit:
                return cuit  # Permitir campo vacío

            # Validar formato de CUIT (11 dígitos)
            if not re.match(r'^\d{11}$', cuit):
                raise ValidationError("El CUIT debe tener 11 dígitos.")

            qs = Contratista.objects.filter(cuit=cuit)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError("Ya existe un contratista con este CUIT.")
            
            return cuit