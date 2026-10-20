from django import forms
from django.core.exceptions import ValidationError
from reservas.models import ActividadDeportiva


class ActividadDeportivaForm(forms.ModelForm):
    """Formulario basado en el modelo ActividadDeportiva para registrar nuevas actividades."""

    class Meta:
        model = ActividadDeportiva
        fields = ('nombre', 'descripcion', 'lugar', 'cupo')
        labels = {
            'nombre': 'Nombre de la actividad',
            'descripcion': 'Descripción',
            'lugar': 'Lugar',
            'cupo': 'Cupo máximo',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la actividad deportiva',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba una descripción de la actividad...',
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el lugar donde se realiza',
            }),
            'cupo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad máxima de participantes',
                'min': 1,
            }),
        }

    def clean_cupo(self):
        cupo = self.cleaned_data.get('cupo')
        if cupo is not None and cupo < 1:
            raise ValidationError('El cupo de la actividad deportiva debe ser mayor a cero.')
        return cupo


class ActividadDeportivaModificaForm(forms.ModelForm):
    """Formulario para modificar una actividad deportiva existente."""

    class Meta:
        model = ActividadDeportiva
        fields = ('nombre', 'descripcion', 'lugar', 'cupo')
        labels = {
            'nombre': 'Nombre de la actividad',
            'descripcion': 'Descripción',
            'lugar': 'Lugar',
            'cupo': 'Cupo máximo',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la actividad deportiva',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escriba una descripción de la actividad...',
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el lugar donde se realiza',
            }),
            'cupo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad máxima de participantes',
                'min': 1,
            }),
        }
