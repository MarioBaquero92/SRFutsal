from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from apps.jugador.forms import FormularioJugador, FormularioDisponibilidad, FormularioUsuario
from apps.jugador.models import Jugador, Disponibilidad




# Create your views here.

def index_jugador(request):
	return render(request, "jugador/index_jugador.html")

class ListaJugador(ListView):
	model = Jugador
	template_name = 'jugador/lista_jugador.html'

class CrearJugador(CreateView):
	model = Jugador
	form_class = FormularioJugador
	second_form_class = FormularioDisponibilidad
	third_form_class = FormularioUsuario
	template_name = 'jugador/formulario_jugador.html'
	success_url = reverse_lazy('jugador:listar_jugadores')

	def get_context_data(self, **kwargs):
		context = super(CrearJugador, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		if 'form3' not in context:
			context['form3'] = self.third_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form_jugador = self.form_class(request.POST)
		form_disponibilidad = self.second_form_class(request.POST)
		form_usuario = self.third_form_class(request.POST)
		if form_jugador.is_valid() and form_disponibilidad.is_valid() and form_usuario.is_valid():
			usuario = form_usuario.save()
			jugador = form_jugador.save(commit=False)
			jugador.user = usuario
			jugador.save()
			disponibilidad = form_disponibilidad.save(commit=False)
			disponibilidad.jugador = jugador
			disponibilidad.save()
			Disponibilidad.objects.filter(pk=disponibilidad.jugador.id).update(jugador=disponibilidad.id)
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form_jugador=form_jugador, form_disponibilidad=form_disponibilidad, form_usuario=form_usuario))


class EditarJugador(UpdateView):
	model = Jugador
	second_model = Disponibilidad
	form_class = FormularioJugador
	second_form_class = FormularioDisponibilidad
	template_name = 'jugador/formulario_jugador.html'
	success_url = reverse_lazy('jugador:listar_jugadores')

	def get_context_data(self, **kwargs):
		context = super(EditarJugador, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		jugador = self.model.objects.get(id=pk)
		disponibilidad = self.second_model.objects.get(jugador=jugador.id)
		print(disponibilidad.id)
		if 'form' not in context:
			context['form'] = self.form_class()
		if 'form2' not in context:
			context['form2'] = self.second_form_class(instance=disponibilidad)
		context['id'] = pk
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_jugador = kwargs['pk']
		jugador = self.model.objects.get(id=id_jugador)
		disponibilidad = self.second_model.objects.get(jugador=jugador.id)
		form = self.form_class(request.POST, instance=jugador)
		form2 = self.second_form_class(request.POST, instance=disponibilidad)

		if form.is_valid() and form2.is_valid():
			form.save()
			form2.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())

class EliminarJugador(DeleteView):
	model = Jugador
	template_name = 'jugador/eliminar_jugador.html'
	success_url = reverse_lazy('jugador:listar_jugadores')
