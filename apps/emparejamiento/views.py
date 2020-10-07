from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse
from django.template import loader
from django.utils import timezone
from apps.emparejamiento.models import Equipo, JugadorEnEquipo, Partido, Calificacion, Confirmacion
from apps.jugador.models import Jugador
from apps.emparejamiento.forms import FormularioEquipo, FormularioJugadorEnEquipo, FormularioPartido, FormularioCalificacion, FormularioConfirmacion
from django.db.models.expressions import RawSQL
from django.db import connection, transaction
from itertools import combinations
import datetime
import pytz
import random
import json
import psycopg2
import pandas as pd
import schedule
import sys
import time
import math

class ListaEquipo(ListView):
	model = Equipo
	template_name = 'emparejamiento/lista_equipo.html'

class CrearEquipo(CreateView):
	model = Equipo
	form_class = FormularioEquipo
	template_name = 'emparejamiento/formulario_equipo.html'
	success_url = reverse_lazy('emparejamiento:listar_equipos')

class EditarEquipo(UpdateView):
	model = Equipo
	form_class = FormularioEquipo
	template_name = 'emparejamiento/formulario_equipo.html'
	success_url = reverse_lazy('emparejamiento:listar_equipos')

class EliminarEquipo(DeleteView):
	model = Equipo
	template_name = 'emparejamiento/eliminar_equipos.html'
	success_url = reverse_lazy('emparejamiento:listar_equipos')

class CrearPartido(CreateView):
	model = Equipo
	form_class = FormularioPartido 
	template_name = 'emparejamiento/formulario_partido.html'	

	def get_context_data(self, **kwargs):
		context = super(CrearPartido, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_equipo1 = request.POST['id_equipo1']
		equipo1 = Equipo.objects.get(id=id_equipo1)

		id_equipo2 = request.POST['id_equipo2']
		equipo2 = Equipo.objects.get(id=id_equipo2)

		fecha = request.POST['fecha']

		jugadores = request.POST.get('jugadores')
		jugadores_dict = json.loads(jugadores)
		tamano_jugadores = len(jugadores_dict)
		todos_jugadores = []

		partidoguardado = Partido(id_equipo1 = equipo1, id_equipo2 = equipo2, fecha = fecha)
		partidoguardado.save()
		idpartido = Partido.objects.latest('id')
		
		for x in range(0,int(tamano_jugadores)):
			jugador = Jugador.objects.get(id=jugadores_dict[x]['pk'])

			if x < 8:
				jugadorenequipo = JugadorEnEquipo(id_jugador = jugador, id_equipo=equipo1, id_partido = idpartido,)
				jugadorenequipo.save()
				todos_jugadores.append(jugador)
			else:
				jugadorenequipo = JugadorEnEquipo(id_jugador = jugador, id_equipo=equipo2, id_partido = idpartido,)
				jugadorenequipo.save()
				todos_jugadores.append(jugador)
		return HttpResponseRedirect(reverse('emparejamiento:listar_partidos'))

def Traer_data(dia_hora):
	cur = connection.cursor()
	cur.execute('''
	CREATE TEMP TABLE JD AS (
	SELECT 
	J.id, J.nombre_completo, J.edad, J.peso, J.estatura, J.perfil,
	J.ritmo, J.tiros, J.pases, J.defensa, J.paradas, J.reflejos, J.posicionamiento,
	D.lun06, D.mar06, D.mie06, D.jue06, D.vie06, D.sab06,
	D.lun07, D.mar07, D.mie07, D.jue07, D.vie07, D.sab07,
	D.lun08, D.mar08, D.mie08, D.jue08, D.vie08, D.sab08,
	D.lun09, D.mar09, D.mie09, D.jue09, D.vie09, D.sab09,
	D.lun10, D.mar10, D.mie10, D.jue10, D.vie10, D.sab10

	FROM	jugador_jugador J INNER JOIN jugador_disponibilidad D ON J.id = D.jugador_id);
	''')

	cur.execute(
		"SELECT id, nombre_completo, edad, peso, estatura, perfil, ritmo, tiros, pases, defensa, paradas, reflejos, posicionamiento FROM JD WHERE "+dia_hora+" = True")
	jugadores_disponibles_dia_hora=cur.fetchall()
   

	df = pd.DataFrame(jugadores_disponibles_dia_hora, columns = ['id', 'nombre_completo', 'edad', 'peso', 'estatura', 'perfil', 'ritmo', 'tiros', 'pases', 'defensa', 'paradas', 'reflejos', 'posicionamiento'])
	POR = df['perfil'] == 'POR'
	DEF = df['perfil'] == 'DEF'
	ATK = df['perfil'] == 'ATK'

	POR = df[POR]
	DEF = df[DEF]
	ATK = df[ATK]

	POR['promedio'] = round(POR.loc[:, 'ritmo':'posicionamiento'].mean(axis=1),2)
	DEF['promedio'] = round(DEF.loc[:, 'ritmo':'posicionamiento'].mean(axis=1),2)
	ATK['promedio'] = round(ATK.loc[:, 'ritmo':'posicionamiento'].mean(axis=1),2)

	POR = POR.loc[:, ['id','nombre_completo','edad', 'peso', 'estatura', 'perfil', 'ritmo', 'tiros', 'pases', 'defensa', 'paradas', 'reflejos', 'posicionamiento', 'promedio']] 
	DEF = DEF.loc[:, ['id','nombre_completo','edad', 'peso', 'estatura', 'perfil', 'ritmo', 'tiros', 'pases', 'defensa', 'paradas', 'reflejos', 'posicionamiento', 'promedio']] 
	ATK = ATK.loc[:, ['id','nombre_completo','edad', 'peso', 'estatura', 'perfil', 'ritmo', 'tiros', 'pases', 'defensa', 'paradas', 'reflejos', 'posicionamiento', 'promedio']] 

	POR = POR.set_index('id').T.to_dict()
	DEF = DEF.set_index('id').T.to_dict()
	ATK = ATK.set_index('id').T.to_dict()

####################################PORTEROS################################

	closest_difference = None

	Todos_Porteros = set(POR.keys())
	for POR_1 in combinations(POR.keys(), 2):
		Porteros_1 = set(POR_1)
		Resto_Porteros = Todos_Porteros - Porteros_1 

		for POR_2 in combinations(Resto_Porteros, 2):
			Porteros_2 = set(POR_2)

		Porteros_Equipo1 = sum([POR[x]['promedio'] for x in Porteros_1])
		Porteros_Equipo2 = sum([POR[x]['promedio'] for x in Porteros_2])

		score_POR = abs(Porteros_Equipo1 - Porteros_Equipo2)

		if not closest_difference or score_POR < closest_difference:
			closest_difference = score_POR
			Porteros_team_a = Porteros_1    
			Porteros_team_b = Porteros_2  

####################################DEFENSAS################################

	closest_difference = None

	Todos_Defensas = set(DEF.keys())
	for DEF_1 in combinations(DEF.keys(), 3):
		Defensas_1 = set(DEF_1)
		Resto_Defensas = Todos_Defensas - Defensas_1 

		for DEF_2 in combinations(Resto_Defensas, 3):
			Defensas_2 = set(DEF_2)

		Defensas_Equipo1 = sum([DEF[x]['promedio'] for x in Defensas_1])
		Defensas_Equipo2 = sum([DEF[x]['promedio'] for x in Defensas_2])

		score_DEF = abs(Defensas_Equipo1 - Defensas_Equipo2)

		if not closest_difference or score_DEF < closest_difference:
			closest_difference = score_DEF
			Defensas_team_a = Defensas_1    
			Defensas_team_b = Defensas_2  

####################################ATACANTES################################

	closest_difference = None


	Todos_Atacantes = set(ATK.keys())
	for ATK_1 in combinations(ATK.keys(), 3):
		Atacantes_1 = set(ATK_1)
		Resto_Atacantes = Todos_Atacantes - Atacantes_1 

		for ATK_2 in combinations(Resto_Atacantes, 3):
			Atacantes_2 = set(ATK_2)

		Atacantes_Equipo1 = sum([ATK[x]['promedio'] for x in Atacantes_1])
		Atacantes_Equipo2 = sum([ATK[x]['promedio'] for x in Atacantes_2])

		score_ATK = abs(Atacantes_Equipo1 - Atacantes_Equipo2)

		if not closest_difference or score_ATK < closest_difference:
			closest_difference = score_ATK
			Atacantes_team_a = Atacantes_1    
			Atacantes_team_b = Atacantes_2  

##############################RESULTADOS#####################################

	prueba = []

	for value in Porteros_team_a:
		aa= POR.get(value)
		dicprueba = {'model': 'jugador.jugador', 'pk' : value, 'fields': aa}
		prueba.append(dicprueba)

	for value in Defensas_team_a:
		aa= DEF.get(value)
		dicprueba = {'model': 'jugador.jugador', 'pk' : value, 'fields': aa}
		prueba.append(dicprueba)

	for value in Atacantes_team_a:
		aa= ATK.get(value)
		dicprueba = {'model': 'jugador.jugador', 'pk' : value, 'fields': aa}
		prueba.append(dicprueba)

	for value in Porteros_team_b:
		aa= POR.get(value)
		dicprueba = {'model': 'jugador.jugador', 'pk' : value, 'fields': aa}
		prueba.append(dicprueba)

	for value in Defensas_team_b:
		aa= DEF.get(value)
		dicprueba = {'model': 'jugador.jugador', 'pk' : value, 'fields': aa}
		prueba.append(dicprueba)


	for value in Atacantes_team_b:
		aa= ATK.get(value)
		dicprueba = {'model': 'jugador.jugador', 'pk' : value, 'fields': aa}
		prueba.append(dicprueba)

	return prueba
		
def GenerarJugador(request):
	dia_y_hora = request.GET['dia_hora']
	data = {
		'jugadores': Traer_data(dia_y_hora)
	}
	print(data)
	return JsonResponse(data)

class ListaPartido(ListView):
	model = Partido
	template_name = 'emparejamiento/lista_partido.html'

class EliminarPartido(DeleteView):
	model = Partido
	template_name = 'emparejamiento/eliminar_partidos.html'
	success_url = reverse_lazy('emparejamiento:listar_partidos')

class FormacionPartido(FormMixin, DetailView):
	model = Partido
	second_model = Calificacion

	form_class = FormularioCalificacion
	template_name = 'emparejamiento/formacion_partido.html'
	success_url = reverse_lazy('emparejamiento:listar_equipos')
	
	def get_context_data(self, **kwargs):
		context = super(FormacionPartido, self).get_context_data(**kwargs)		
		partido_id = self.kwargs['pk']
		partido = Partido.objects.get(id=partido_id)	
		validarPartido(partido)
		cur = connection.cursor()
		cur.execute('SELECT * FROM jugador_jugador WHERE id in (SELECT id_jugador_id FROM emparejamiento_jugadorenequipo WHERE id_equipo_id = (SELECT id_equipo1_id FROM emparejamiento_partido WHERE id = '+partido_id+') and id_partido_id = '+partido_id+')')
		jugadores1_columns = [column[0] for column in cur.description]
		jugadores1 = []
		for row in cur.fetchall():
			jugadores1.append(dict(zip(jugadores1_columns, row)))
		cur.execute('SELECT * FROM jugador_jugador WHERE id in (SELECT id_jugador_id FROM emparejamiento_jugadorenequipo WHERE id_equipo_id = (SELECT id_equipo2_id FROM emparejamiento_partido WHERE id = '+partido_id+') and id_partido_id = '+partido_id+')')
		jugadores2_columns = [column[0] for column in cur.description]
		jugadores2 = []
		for row in cur.fetchall():
			jugadores2.append(dict(zip(jugadores2_columns, row)))
		user = self.request.user
		puedeCalificar = False
		calificaciones = []
		if hasattr(user, 'jugador'):
			calificaciones = Calificacion.objects.all().filter(calificador = user.jugador.id)
		print(calificaciones)
		for jugador in jugadores1:
			for calificacion in calificaciones:
				if jugador.get('id') == calificacion.jugador.id:
					jugador['id_calificacion'] = calificacion.id
					jugador['valor_calificacion'] = calificacion.calificacion
			if jugador.get('user_id') == user.id:
				puedeCalificar = True
		for jugador in jugadores2:
			for calificacion in calificaciones:
				if jugador.get('id') == calificacion.jugador.id:
					jugador['id_calificacion'] = calificacion.id
					jugador['valor_calificacion'] = calificacion.calificacion
			if jugador.get('user_id') == user.id:
				puedeCalificar = True
		context['jugadores1'] = jugadores1
		context['jugadores2'] = jugadores2
		if (partido.estado != "jugado"):
			puedeCalificar = False
		if hasattr(user, 'jugador'):
			context['id_jugador_actual'] = user.jugador.id
		context['puedeCalificar'] = puedeCalificar
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_calificacion = request.POST['id_calificacion']
		id_partido = request.POST['id_partido']
		id_jugador = request.POST['id_jugador']
		id_calificador = request.POST['id_calificador']
		calificacion = request.POST['calificacion']
		partido = Partido.objects.get(id=id_partido)
		jugador = Jugador.objects.get(id=id_jugador)
		calificador = Jugador.objects.get(id=id_calificador)
		if int(id_calificacion) == -1:
			calificacion = Calificacion(id_partido = partido, jugador= jugador, calificador = calificador, calificacion = calificacion)		
			calificacion.save()
		else:
			calificacion = Calificacion(id=id_calificacion, id_partido = partido, jugador= jugador, calificador = calificador, calificacion = calificacion)
			calificacion.save()
		return HttpResponseRedirect(self.get_success_url())

class JugadoresEquipo(ListView):
	model = JugadorEnEquipo
	template_name = 'emparejamiento/listado_jugadores_en_equipo.html'

class CrearConfirmacion(CreateView):
	model = Confirmacion
	form_class = FormularioConfirmacion
	template_name = 'emparejamiento/confirmacion_partido.html'
	success_url = reverse_lazy('emparejamiento:listar_jugadorequipo')

	def get(self, request, *args, **kwargs):
		id_jugador = self.kwargs['pk']
		jugadorEnEquipo = JugadorEnEquipo.objects.get(id=id_jugador)
		existe_confirmacion = Confirmacion.objects.filter(id_jugador=id_jugador).count()
		if existe_confirmacion > 0:
			self.object = self.model.objects.get(id_jugador=id_jugador)
		else:
			self.object = Confirmacion()
		return self.render_to_response(self.get_context_data())

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_jugador = self.kwargs['pk']
		jugadorEnEquipo = JugadorEnEquipo.objects.get(id=id_jugador)
		form_confirmacion = self.form_class(request.POST)
		if form_confirmacion.is_valid():
			existe_confirmacion = Confirmacion.objects.filter(id_jugador=id_jugador).count()
			if existe_confirmacion > 0:
				confirmacion_existente = Confirmacion.objects.get(id_jugador=id_jugador)
			else:
				confirmacion_existente = Confirmacion()
			confirmacion_existente.id_jugador=jugadorEnEquipo
			confirmacion_existente.confirmo=form_confirmacion.cleaned_data['confirmo']
			confirmacion_existente.save()
			validarPartido(jugadorEnEquipo.id_partido)
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form_class=form_confirmacion))

def validarPartido(partido):
	confirmaciones = Confirmacion.objects.filter(id_jugador__id_partido_id=partido.id)
	fecha_actual = timezone.now()
	if (len(confirmaciones) >= 10): 
		bandera_equipo1 = confirmaciones[0].id_jugador.id_equipo.id
		contador_equipo1 = 0
		contador_equipo2 = 0
		for i in range(len(confirmaciones)):
			if(confirmaciones[i].id_jugador.id_equipo.id == bandera_equipo1):
				contador_equipo1 += 1
			else:
				contador_equipo2 += 1
		if( contador_equipo1 >= 5 and contador_equipo2 >= 5):
			if(fecha_actual >= partido.fecha):
				partido.estado = "jugado"
				partido.save()
			else:
				partido.estado = "por jugar"
				partido.save()
	else:
		if(fecha_actual >= partido.fecha):
			partido.estado = "cancelado"
			partido.save()
