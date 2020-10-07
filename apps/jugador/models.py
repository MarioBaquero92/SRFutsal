from django.db import models
from django.contrib.auth.models import User
#from multiselectfield import MultiSelectField

# Create your models here.

class Jugador(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default= None)
	nombre_completo = models.CharField(max_length=50)
	edad = models.PositiveSmallIntegerField()
	peso = models.PositiveSmallIntegerField()
	estatura = models.PositiveSmallIntegerField()
	perfil = models.CharField(max_length=3)
	ritmo = models.PositiveSmallIntegerField()
	tiros = models.PositiveSmallIntegerField()
	pases = models.PositiveSmallIntegerField()
	defensa = models.PositiveSmallIntegerField()
	paradas = models.PositiveSmallIntegerField()
	reflejos = models.PositiveSmallIntegerField()
	posicionamiento = models.PositiveSmallIntegerField()	
	
	def __str__(self):
		return '{}'.format(self.nombre_completo, self.nombre_completo)

class Disponibilidad(models.Model):
	jugador = models.ForeignKey(Jugador, null=True, blank=True, on_delete=models.CASCADE)
	
	lun06 = models.BooleanField(default=False)
	mar06 = models.BooleanField(default=False)
	mie06 = models.BooleanField(default=False)
	jue06 = models.BooleanField(default=False)
	vie06 = models.BooleanField(default=False)
	sab06 = models.BooleanField(default=False)

	lun07 = models.BooleanField(default=False)
	mar07 = models.BooleanField(default=False)
	mie07 = models.BooleanField(default=False)
	jue07 = models.BooleanField(default=False)
	vie07 = models.BooleanField(default=False)
	sab07 = models.BooleanField(default=False)

	lun08 = models.BooleanField(default=False)
	mar08 = models.BooleanField(default=False)
	mie08 = models.BooleanField(default=False)
	jue08 = models.BooleanField(default=False)
	vie08 = models.BooleanField(default=False)
	sab08 = models.BooleanField(default=False)

	lun09 = models.BooleanField(default=False)
	mar09 = models.BooleanField(default=False)
	mie09 = models.BooleanField(default=False)
	jue09 = models.BooleanField(default=False)
	vie09 = models.BooleanField(default=False)
	sab09 = models.BooleanField(default=False)

	lun10 = models.BooleanField(default=False)
	mar10 = models.BooleanField(default=False)
	mie10 = models.BooleanField(default=False)
	jue10 = models.BooleanField(default=False)
	vie10 = models.BooleanField(default=False)
	sab10 = models.BooleanField(default=False)
	
