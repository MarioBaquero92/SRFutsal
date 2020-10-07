from django.db import models
from apps.jugador.models import Jugador
from datetime import datetime    

# Create your models here.


class Equipo(models.Model):
	nombre_equipo = models.CharField(max_length=20)
	def __str__(self):
		return '{}'.format(self.nombre_equipo)
		

class Partido(models.Model):
	id_equipo1		= models.ForeignKey(Equipo, null=False, blank=False, on_delete=models.CASCADE, related_name='equipo_equipo1')
	id_equipo2		= models.ForeignKey(Equipo, null=False, blank=False, on_delete=models.CASCADE, related_name='equipo_equipo2')
	fecha			= models.DateTimeField(default=datetime.now, blank=True)
	estado			= models.CharField(max_length=10,default='por jugar')

class JugadorEnEquipo(models.Model):
	id_jugador 		= models.ForeignKey(Jugador, null=False, blank=False, on_delete=models.CASCADE, related_name='id_jugador')
	id_equipo 		= models.ForeignKey(Equipo, null=False, blank=False, on_delete=models.CASCADE, related_name='id_equipo')
	fecha 			= models.DateField(auto_now=True)
	id_partido 		= models.ForeignKey(Partido, null=False, blank=False, on_delete=models.CASCADE, related_name='id_partido')


puntuacion = (
              ('1', '1'),
              ('2', '2'),
              ('3', '3'),
              ('4', '4'),
              ('5', '5'),
    		)

class Calificacion(models.Model):
	id_partido		= models.ForeignKey(Partido, null=False, blank=False, on_delete=models.CASCADE, related_name='calificacion_partido')
	calificacion 	= models.PositiveSmallIntegerField()
	fecha 			= models.DateField(auto_now=True)
	jugador			= models.ForeignKey(Jugador, null=True, blank=True, on_delete=models.CASCADE, related_name='calificacion_jugador')
	calificador		= models.ForeignKey(Jugador, null=True, blank=True, on_delete=models.CASCADE, related_name='calificacion_calificador')
#	id_jugador 		= models.ForeignKey(JugadorEnEquipo, null=False, blank=False, on_delete=models.CASCADE, related_name='calificacion_jugador')

#	calificacion= models.CharField(max_length=20, choices=puntuacion, default='1') 

class Confirmacion(models.Model):
	id_jugador = models.ForeignKey(JugadorEnEquipo, null=False, blank=False, on_delete=models.CASCADE, related_name='id_confirmador')
	confirmo 			= models.BooleanField(default=False)