from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario,Actividad, Cuadrilla, EmpleadoCuadrilla

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = Usuario
		fields = ['username','first_name','last_name', 'rol', 'email', 'password1', 'password2','identificacion','estado']
	def clean_email(self):
		email = self.cleaned_data['email']

		if Usuario.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre_actividad', 'detalles', 'imagen', 'estado','id_colonia', 'id_cuadrilla', 'id_usuario']


class CuadrillaForm(forms.ModelForm):
    class Meta:
        model = Cuadrilla
        fields = ['numero_cuadrilla', 'jefe_cuadrilla', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empleados'] = forms.ModelMultipleChoiceField(
            queryset=Usuario.objects.filter(rol='EMPLEADO'),
            required=False,
            widget=forms.SelectMultiple
        )

class EmpleadoCuadrillaForm(forms.ModelForm):
    class Meta:
        model = EmpleadoCuadrilla
        fields = ['cuadrilla', 'empleado']  