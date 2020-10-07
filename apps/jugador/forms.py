from django import forms
from apps.jugador.models import Jugador, Disponibilidad

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class FormularioUsuario(UserCreationForm):
	class Meta:
		model = User
		fields = [
				'username'
		]

		labels = {
				'username':'Nombre de usuario'
		}
# class FormularioUsuario(forms.ModelForm):
# 	class Meta:
# 		model = User
# 		fields = [
# 				'username',
# 				'password'
# 		]

# 		labels = {
# 				'username':'Nombre de usuario',
# 				'password':'Contraseña'
# 		}

# 		widgets = {
# 		'username': forms.TextInput(attrs={'class':'form-control'}),
# 		'password': forms.PasswordInput(attrs={'class':'form-control'})
# 		}

class FormularioJugador(forms.ModelForm):
	
	class Meta:
		PERFIL = (
            ('POR', 'Portero'),
            ('DEF', 'Defensivo'),
            ('ATK', 'Atacante'),)


		model = Jugador

		fields = [
		'nombre_completo',
		'edad',
		'peso',
		'estatura',
		'perfil',
		'ritmo',
		'tiros',
		'pases',
		'defensa',
		'paradas',
		'reflejos',
		'posicionamiento',
		# 'disponibilidad',
		]

		labels = {
		'nombre_completo': 'Nombre y apellido',
		'edad': 'Edad', 
		'peso': 'Peso (Kg)',
		'estatura': 'Estatura (cm)',
		'perfil': 'Perfil',
		'ritmo': 'Ritmo',
		'tiros': 'Tiros',
		'pases': 'Pases',
		'defensa': 'Defensa',
		'paradas': 'Paradas',
		'reflejos': 'Reflejos',
		'posicionamiento': 'Posicionamiento',
		# 'disponibilidad':'Disponibilidad',
		}

		

		widgets = {
		'nombre_completo': forms.TextInput(attrs={'class':'form-control'}),
		'edad': forms.TextInput( attrs={'class':'form-control','type':'number'}),
		'peso': forms.TextInput(attrs={'class':'form-control','type':'number'}),
		'estatura': forms.TextInput(attrs={'class':'form-control','type':'number'}),
		'perfil': forms.Select(choices=PERFIL, attrs={'class':'form-control'}),
		'ritmo': forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
		'tiros': forms.TextInput(attrs={'class':'form-control','type':'number'}),
		'pases': forms.TextInput(attrs={'class':'form-control','type':'number'}),
		'defensa': forms.TextInput(attrs={'class':'form-control','type':'number'}),
		'paradas': forms.TextInput(attrs={'class':'form-control','type':'number'}),
		'reflejos': forms.TextInput(attrs={'class':'form-control','type':'number'}),
		'posicionamiento': forms.TextInput(attrs={'class':'form-control','type':'number'}),
		# 'disponibilidad': forms.TextInput(attrs={'class':'form-control'}),
		
		}


class FormularioDisponibilidad(forms.ModelForm):
	class Meta:
		model = Disponibilidad

		fields = [
#		'jugador',
		'lun06','mar06','mie06','jue06','vie06','sab06',
		'lun07','mar07','mie07','jue07','vie07','sab07',
		'lun08','mar08','mie08','jue08','vie08','sab08',
		'lun09','mar09','mie09','jue09','vie09','sab09',
		'lun10','mar10','mie10','jue10','vie10','sab10',
		]

		labels = {
#		'jugador':'Id_Jugador Oculto',
		'lun06':'Lunes 06:00Pm', 'mar06':'Martes 06:00Pm', 'mie06':'Miércoles 06:00Pm', 'jue06':'Jueves 06:00Pm', 'vie06':'Viernes 06:00Pm', 'sab06':'Sabado 06:00Pm',
		'lun07':'Lunes 07:00Pm', 'mar07':'Martes 07:00Pm', 'mie07':'Miércoles 07:00Pm', 'jue07':'Jueves 07:00Pm', 'vie07':'Viernes 07:00Pm', 'sab07':'Sabado 07:00Pm',
		'lun08':'Lunes 08:00Pm', 'mar08':'Martes 08:00Pm', 'mie08':'Miércoles 08:00Pm', 'jue08':'Jueves 08:00Pm', 'vie08':'Viernes 08:00Pm', 'sab08':'Sabado 08:00Pm',
		'lun09':'Lunes 09:00Pm', 'mar09':'Martes 09:00Pm', 'mie09':'Miércoles 09:00Pm', 'jue09':'Jueves 09:00Pm', 'vie09':'Viernes 09:00Pm', 'sab09':'Sabado 09:00Pm',
		'lun10':'Lunes 10:00Pm', 'mar10':'Martes 10:00Pm', 'mie10':'Miércoles 10:00Pm', 'jue10':'Jueves 10:00Pm', 'vie10':'Viernes 10:00Pm', 'sab10':'Sabado 10:00Pm',
		}

		widgets = {
#		'juagdor':forms.HiddenInput(),
		'lun06':forms.CheckboxInput(attrs={'class':'form-control'}), 'mar06':forms.CheckboxInput(attrs={'class':'form-control'}), 'mie06':forms.CheckboxInput(attrs={'class':'form-control'}),
		'lun07':forms.CheckboxInput(attrs={'class':'form-control'}), 'mar07':forms.CheckboxInput(attrs={'class':'form-control'}), 'mie07':forms.CheckboxInput(attrs={'class':'form-control'}),
		'lun08':forms.CheckboxInput(attrs={'class':'form-control'}), 'mar08':forms.CheckboxInput(attrs={'class':'form-control'}), 'mie08':forms.CheckboxInput(attrs={'class':'form-control'}),
		'lun09':forms.CheckboxInput(attrs={'class':'form-control'}), 'mar09':forms.CheckboxInput(attrs={'class':'form-control'}), 'mie09':forms.CheckboxInput(attrs={'class':'form-control'}),
		'lun10':forms.CheckboxInput(attrs={'class':'form-control'}), 'mar10':forms.CheckboxInput(attrs={'class':'form-control'}), 'mie10':forms.CheckboxInput(attrs={'class':'form-control'}),

		'jue06':forms.CheckboxInput(attrs={'class':'form-control'}), 'vie06':forms.CheckboxInput(attrs={'class':'form-control'}), 'sab06':forms.CheckboxInput(attrs={'class':'form-control'}),
 		'jue07':forms.CheckboxInput(attrs={'class':'form-control'}), 'vie07':forms.CheckboxInput(attrs={'class':'form-control'}), 'sab07':forms.CheckboxInput(attrs={'class':'form-control'}),
 		'jue08':forms.CheckboxInput(attrs={'class':'form-control'}), 'vie08':forms.CheckboxInput(attrs={'class':'form-control'}), 'sab08':forms.CheckboxInput(attrs={'class':'form-control'}),
 		'jue09':forms.CheckboxInput(attrs={'class':'form-control'}), 'vie09':forms.CheckboxInput(attrs={'class':'form-control'}), 'sab09':forms.CheckboxInput(attrs={'class':'form-control'}),
 		'jue10':forms.CheckboxInput(attrs={'class':'form-control'}), 'vie10':forms.CheckboxInput(attrs={'class':'form-control'}), 'sab10':forms.CheckboxInput(attrs={'class':'form-control'}),
		}

	
	
		