from django import forms
from apps.emparejamiento.models import Equipo, JugadorEnEquipo, Partido, Calificacion, Confirmacion



class FormularioEquipo(forms.ModelForm):
	class Meta:
		model = Equipo

		fields = [
		'nombre_equipo',
		]

		labels = {
		'nombre_equipo': 'Nombre del Equipo',
		}

		widgets = {
		'nombre_equipo': forms.TextInput(attrs={'class':'form-control'}),
		}

class FormularioJugadorEnEquipo(forms.ModelForm):
	class Meta:
		model = JugadorEnEquipo

		fields = [
		'id_jugador',
		'id_equipo',

		# 'fecha',
		]

		labels = {
		'id_jugador': 'Id Jugador',
		'id_equipo': 'Id Equipo',
		# 'fecha': 'Fecha',
		}

		widgets = {
		'id_jugador':forms.TextInput(attrs={'class':'form-control'}),
		'id_equipo':forms.TextInput(attrs={'class':'form-control'}),
		# 'fecha': forms.TextInput(attrs={'class':'form-control'}),
		}
		
class FormularioPartido(forms.ModelForm):
	class Meta:
		model = Partido

		fields = [
		'id_equipo1',
		'id_equipo2',
		# 'fecha',
		]

		labels = {
		'id_equipo1': 'Nombre Equipo Local',
		'id_equipo2': 'Nombre Equipo Visitante',
		# 'fecha': 'Fecha',
		}

		widgets = {
		'id_equipo1': forms.Select(attrs={'class':'form-control'}),
		'id_equipo2': forms.Select(attrs={'class':'form-control'}),
		# 'fecha': forms.TextInput(attrs={'class':'form-control'}),
		}



class FormularioCalificacion(forms.ModelForm):
	class Meta:
		CHOICES = (
            ('', 'Seleccionar'),
            ('1', 'Pesima'),
            ('2', 'Mal'),
            ('3', 'Regular'),
            ('4', 'Buena'),
            ('5', 'Excelente'),)

		model = Calificacion

		fields = [
		'calificacion',
		'id_partido',
		'jugador',
		'calificador',
		'id'
		]

		labels = {
		'calificacion': 'Califica el rendimiento del Jugador',
		'id_partido': 'partidocalid',
		}

		widgets = {
		'calificacion': forms.Select(choices=CHOICES),
		'id_partido': forms.HiddenInput(attrs={'class':'form-control'}),
		'jugador': forms.HiddenInput(attrs={'class':'form-control'}),
		'calificador': forms.HiddenInput(attrs={'class':'form-control'}),
		'id': forms.HiddenInput(attrs={'class':'form-control'}),
		}

class FormularioConfirmacion(forms.ModelForm):
	class Meta:
		model = Confirmacion

		fields = [
			'confirmo',
		]

		labels = {
			'confirmo': '¿Podrá jugar este partido?',
		}

		widgets = {
			'confirmo':forms.CheckboxInput(attrs={'class':'form-control'}),
		}
 